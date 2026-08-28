# Dialogue text translation (summary compression method)
# Keeps I/O compatibility with experimental/01/translate.py (sliding window)
# while following the summary compression architecture of
# experimental/01/translate-json.py.
# Activates the KV cache by keeping chat_history in a fixed
# system + summary + most recent KEEP pairs structure.

import argparse
import json
import time
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema

parser = argparse.ArgumentParser(description="Translate dialogue text using the summary compression method")
parser.add_argument("input_file", help="Text file to translate")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="Source language (e.g. French, English, Japanese)")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="Target language (e.g. Spanish, Japanese)")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="Output file name")
parser.add_argument("-m", "--model", required=True, help="Translation model")
parser.add_argument("--threshold", type=int, default=10, help="Interval (in translation pairs) between summary generations (default: 10)")
parser.add_argument("--keep", type=int, default=5, help="Number of most recent pairs kept after compression (default: 5)")
parser.add_argument("--summary", choices=["glossary"], default=None,
                    help="Summary method: glossary=proper nouns + content summary. If unspecified, simple deletion (fastest)")
parser.add_argument("--no-think", action="store_true", help="Disable thinking (for Qwen3 models)")
parser.add_argument("--schema", action="store_true", help="Enable structured output (JSON schema)")
parser.add_argument("--no-summary-history", action="store_true",
                    help="Do not keep the summary in chat_history (only inject it at compression time)")
args = parser.parse_args()

MODEL = args.model
THRESHOLD = args.threshold
KEEP = args.keep
SUMMARY_TYPE = args.summary
THINK = not args.no_think
SUMMARY_IN_HISTORY = not args.no_summary_history


class Translation(BaseModel):
    translation: str = Field(description=f"Direct translation from {args.from_lang} to {args.to_lang}")

SCHEMA = Translation if args.schema else None

with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Only lines where a speaker can be split off are translated
entries = []
for line in lines:
    line = line.strip()
    if not line or ":" not in line:
        continue
    speaker, text = line.split(":", 1)
    entries.append((speaker.strip(), text.strip()))

system_message = {
    "role": "system",
    "content": (
        f"You are a professional translator. Translate the following {args.from_lang} "
        f"text to {args.to_lang}. Maintain consistency with previous translations and "
        f"preserve the context and nuance of the original text. Provide only the "
        f"translation without any explanations or commentary."
    ),
}


def call_llm(prompt, schema=None):
    """Append prompt to chat_history, call the LLM, and add the response to history as well."""
    user_message = {"role": "user", "content": prompt}
    chat_history.append(user_message)

    response = generate_with_schema(
        chat_history,
        schema=schema,
        model=MODEL,
        include_thoughts=THINK,
        show_params=False,
    )
    response_text = response.text.strip()

    chunk = response.chunks[-1] if response.chunks else None
    if chunk and hasattr(chunk, "prompt_eval_count") and chunk.prompt_eval_count:
        prompt_dur = chunk.prompt_eval_duration / 1e9
        prompt_tps = chunk.prompt_eval_count / prompt_dur
        eval_dur   = chunk.eval_duration / 1e9
        eval_tps   = chunk.eval_count / eval_dur
        total_dur  = chunk.total_duration / 1e9
        print(f"  prompt: {chunk.prompt_eval_count} tokens, {prompt_dur:.2f}s, {prompt_tps:.0f} tps"
              f" | eval: {chunk.eval_count} tokens, {eval_dur:.2f}s, {eval_tps:.0f} tps"
              f" | total: {total_dur:.2f}s")

    assistant_message = {"role": "assistant", "content": response_text}
    chat_history.append(assistant_message)

    return response_text, user_message, assistant_message


def summarize_messages(summary_type):
    """Generate a summary. Appending to chat_history is handled by call_llm."""
    if summary_type == "glossary":
        summary_content = (
            "Please compress the translation history above into a concise summary "
            "with two parts.\n\n"
            "PART 1 - Proper noun glossary:\n"
            "List original→translated mappings for:\n"
            "- Person names, place names, work/product titles\n"
            "- Domain-specific technical terms with their chosen translations\n"
            "Do NOT include speaking styles, tone, or expression patterns.\n\n"
            "PART 2 - Content summary (English, 2-3 sentences):\n"
            "Summarize what was discussed. Focus on topics and narrative context, "
            "not on how things were phrased.\n\n"
            "If a previous summary exists, integrate the new content with it rather "
            "than starting over."
        )
    else:
        raise ValueError(f"Unknown summary type: {summary_type}")

    return call_llm(summary_content)


translation_messages = []       # Cumulative translation (U, A) pairs (never-deleted ledger)
summary_messages = []           # Cumulative summary (U, A) pairs
chat_history = [system_message] # The context actually passed to the LLM
next_compression = None

translations = []
start_time = time.time()

total = len(entries)
for i, (speaker, text) in enumerate(entries, 1):
    prompt = (
        f"Translate the following {args.from_lang} line spoken by {speaker} "
        f"into {args.to_lang}.\n{text}"
    )
    print(f"[{i}/{total}] {speaker}")
    raw, user_message, assistant_message = call_llm(prompt, schema=SCHEMA)
    translated_text = json.loads(raw)["translation"] if SCHEMA is not None else raw

    translation_messages.append(user_message)
    translation_messages.append(assistant_message)

    translations.append((speaker, translated_text))

    # Schedule summary generation: after completing translation 10, 20, 30, ...
    if i % THRESHOLD == 0:
        next_compression = i + KEEP if i + KEEP <= len(entries) else None

        if SUMMARY_TYPE is not None and next_compression is not None:
            print(f"[Generating summary after translation {i}]")
            saved_len = len(chat_history)
            _, sum_req, sum_res = summarize_messages(SUMMARY_TYPE)
            if not SUMMARY_IN_HISTORY:
                del chat_history[saved_len:]
            summary_messages.append(sum_req)
            summary_messages.append(sum_res)

    # Compression: after completing translation 15, 25, 35, ...
    if next_compression is not None and i == next_compression:
        print(f"[Compressing history after translation {i}: keeping {KEEP} pairs]")
        if SUMMARY_TYPE is None:
            chat_history = [system_message] + translation_messages[-KEEP * 2:]
        else:
            chat_history = [system_message] + summary_messages[-2:] + translation_messages[-KEEP * 2:]

elapsed = time.time() - start_time

with open(args.output_file, "w", encoding="utf-8") as f:
    for speaker, translation in translations:
        f.write(f"{speaker}: {translation}\n")

print(f"\nTranslation complete: {args.from_lang} → {args.to_lang} ({args.output_file})")
print(f"Processing time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
