# Dialogue text translation (term pre-extraction approach)
# Building on the structure of experimental/03, this extracts terms and proper nouns
# from the full text before translation starts and fixes their translations up front.
# On every reorganization, a "term list scoped to the target range" is injected into
# chat_history. CoT is not used (translation, summarization, extraction, and
# translation generation all run with think=False).

import argparse
import json
import os
import sys
import time
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema

parser = argparse.ArgumentParser(description="Translate dialogue text using term pre-extraction")
parser.add_argument("input_file", help="Text file to translate")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="Source language (e.g., French, English, Japanese)")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="Target language (e.g., Spanish, Japanese)")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="Output file name")
parser.add_argument("-m", "--model", required=True, help="Translation model")
parser.add_argument("--threshold", type=int, default=10, help="Interval for generating a summary (default: 10)")
parser.add_argument("--keep", type=int, default=5, help="Number of translation pairs kept between a summary and the next reorganization (default: 5)")
parser.add_argument("--terms", dest="terms_file", default=None,
                    help="Path to the term file (default: <output_base>-terms.json)")
parser.add_argument("--terms-only", action="store_true",
                    help="Run only term extraction and translation generation, then exit (no translation)")
args = parser.parse_args()

MODEL = args.model
THRESHOLD = args.threshold
KEEP = args.keep
FROM_LANG = args.from_lang
TO_LANG = args.to_lang

if args.terms_file:
    TERMS_FILE = args.terms_file
else:
    base, _ = os.path.splitext(args.output_file)
    TERMS_FILE = f"{base}-terms.json"


class TermList(BaseModel):
    terms: list[str] = Field(
        description="Proper nouns and domain-specific technical terms in the original source language"
    )


class TermPair(BaseModel):
    original: str = Field(description="The term in the source language")
    translation: str = Field(description="The translated term in the target language")


class Glossary(BaseModel):
    glossary: list[TermPair]


with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

entries = []
for line in lines:
    line = line.strip()
    if not line or ":" not in line:
        continue
    speaker, text = line.split(":", 1)
    entries.append((speaker.strip(), text.strip()))

total = len(entries)


def chunk_range(chunk_index):
    """1-indexed chunk_index → (start_entry, end_entry), both 1-indexed inclusive."""
    start = (chunk_index - 1) * KEEP + 1
    end = min(chunk_index * KEEP, total)
    return start, end


def num_chunks():
    return (total + KEEP - 1) // KEEP


def print_response_stats(response):
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


def call_with_schema(prompts, schema):
    """A single-shot structured output call (no history). Retries up to 3 times on JSON errors."""
    max_retries = 3
    for attempt in range(max_retries):
        response = generate_with_schema(
            prompts,
            schema=schema,
            model=MODEL,
            include_thoughts=False,
            show_params=False,
        )
        try:
            data = json.loads(response.text)
            print_response_stats(response)
            return data
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                print(f"  JSON decode error (attempt {attempt+1}/{max_retries}): {e}")
                time.sleep(3)
            else:
                raise


def extract_terms(chunk_text):
    """Extract source-language terms from a single chunk."""
    prompt = (
        f"Extract proper nouns and domain-specific technical terms from the following "
        f"{FROM_LANG} text. Return them in the original {FROM_LANG} form (do NOT translate).\n\n"
        f"Include:\n"
        f"- Person names, place names, organization names\n"
        f"- Work titles, product names, brand names\n"
        f"- Domain-specific technical terms and jargon\n\n"
        f"Exclude:\n"
        f"- Common everyday words and general vocabulary\n"
        f"- Pronouns, articles, conjunctions, prepositions\n"
        f"- Speaking styles or expressions\n\n"
        f"Output each term in its base form WITHOUT leading articles "
        f"(e.g., output 'affinage', not 'l'affinage' or 'le affinage').\n\n"
        f"Text:\n{chunk_text}"
    )
    data = call_with_schema([prompt], TermList)
    return data.get("terms", [])


def translate_glossary(originals):
    """Translate all terms in a single batch."""
    if not originals:
        return {}
    listing = "\n".join(f"- {t}" for t in originals)
    prompt = (
        f"Translate the following {FROM_LANG} terms into {TO_LANG}. "
        f"Provide a translation for every term. If a term is a proper noun "
        f"(e.g., person name) that should remain unchanged, output it as-is.\n\n"
        f"Terms:\n{listing}"
    )
    data = call_with_schema([prompt], Glossary)
    pairs = data.get("glossary", [])
    mapping = {p["original"]: p["translation"] for p in pairs}
    for orig in originals:
        if orig not in mapping:
            print(f"  WARNING: glossary missing translation for '{orig}', using original.")
            mapping[orig] = orig
    return mapping


def write_terms_file(path, chunk_terms_map, translations):
    """Write the term file as JSON."""
    data = {
        "from": FROM_LANG,
        "to": TO_LANG,
        "chunks": [
            {"index": cidx, "start": chunk_range(cidx)[0], "end": chunk_range(cidx)[1],
             "terms": chunk_terms_map[cidx]}
            for cidx in sorted(chunk_terms_map.keys())
        ],
        "glossary": translations,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_terms_file(path):
    """Load the term file (JSON) and return (chunk_terms_map, translations)."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("from") != FROM_LANG:
        raise ValueError(
            f"Term file's from language ({data.get('from')}) does not match the argument ({FROM_LANG}): {path}"
        )
    if data.get("to") != TO_LANG:
        raise ValueError(
            f"Term file's to language ({data.get('to')}) does not match the argument ({TO_LANG}): {path}"
        )

    chunk_terms_map = {c["index"]: c["terms"] for c in data.get("chunks", [])}
    translations = data.get("glossary", {})
    return chunk_terms_map, translations


# Phase 0: term extraction and translation generation
if os.path.exists(TERMS_FILE):
    print(f"Loading existing term file: {TERMS_FILE}")
    chunk_terms_map, term_translations = read_terms_file(TERMS_FILE)
else:
    print(f"Starting term extraction: {num_chunks()} chunks (keep={KEEP})")
    chunk_terms_map = {}
    for cidx in range(1, num_chunks() + 1):
        start, end = chunk_range(cidx)
        chunk_text = "\n".join(f"{sp}: {tx}" for sp, tx in entries[start - 1:end])
        print(f"[Extract chunk {cidx}: lines {start}-{end}]")
        chunk_terms_map[cidx] = extract_terms(chunk_text)

    seen = set()
    unique_terms = []
    for cidx in sorted(chunk_terms_map.keys()):
        for t in chunk_terms_map[cidx]:
            if t not in seen:
                seen.add(t)
                unique_terms.append(t)

    print(f"[Translating glossary: {len(unique_terms)} unique terms]")
    term_translations = translate_glossary(unique_terms)

    write_terms_file(TERMS_FILE, chunk_terms_map, term_translations)
    print(f"Saved term file: {TERMS_FILE}")

if args.terms_only:
    sys.exit(0)


def build_terms_messages(start_entry, end_entry):
    """Return the message pair for terms appearing within the given range (1-indexed inclusive)."""
    chunks_in_range = []
    for cidx in sorted(chunk_terms_map.keys()):
        cstart, cend = chunk_range(cidx)
        if cstart <= end_entry and cend >= start_entry:
            chunks_in_range.append(cidx)

    seen = set()
    relevant = []
    for cidx in chunks_in_range:
        for t in chunk_terms_map[cidx]:
            if t not in seen:
                seen.add(t)
                relevant.append(t)

    if not relevant:
        return []

    listing = "\n".join(f"{t} => {term_translations.get(t, t)}" for t in relevant)
    user_msg = {
        "role": "user",
        "content": (
            f"Glossary for the upcoming {FROM_LANG} → {TO_LANG} translation. "
            f"Use these translations consistently:\n{listing}"
        ),
    }
    assistant_msg = {
        "role": "assistant",
        "content": "Acknowledged. I will use these translations consistently.",
    }
    return [user_msg, assistant_msg]


# Phase 1: translation loop
system_message = {
    "role": "system",
    "content": (
        f"You are a professional translator. Translate the following {FROM_LANG} "
        f"text to {TO_LANG}. Maintain consistency with previous translations and "
        f"preserve the context and nuance of the original text. Provide only the "
        f"translation without any explanations or commentary."
    ),
}


def call_llm(prompt):
    """Append prompt to chat_history, call the LLM, and also append the response to history."""
    user_message = {"role": "user", "content": prompt}
    chat_history.append(user_message)

    response = generate_with_schema(
        chat_history,
        model=MODEL,
        include_thoughts=False,
        show_params=False,
    )
    response_text = response.text.strip()
    print_response_stats(response)

    assistant_message = {"role": "assistant", "content": response_text}
    chat_history.append(assistant_message)

    return response_text, user_message, assistant_message


def summarize_messages():
    """Generate a content summary (no CoT). Terms and proper nouns are already pre-extracted, so they are not included."""
    summary_content = (
        "Please summarize the translation history above in 2-3 sentences (in English). "
        "Focus on topics and narrative context. "
        "If a previous summary exists, integrate the new content with it rather "
        "than starting over."
    )
    return call_llm(summary_content)


translation_messages = []
summary_messages = []
chat_history = [system_message] + build_terms_messages(1, min(THRESHOLD + KEEP, total))
next_compression = None

translations = []
start_time = time.time()

for i, (speaker, text) in enumerate(entries, 1):
    prompt = (
        f"Translate the following {FROM_LANG} line spoken by {speaker} "
        f"into {TO_LANG}.\n{text}"
    )
    print(f"[{i}/{total}] {speaker}")
    translated_text, user_message, assistant_message = call_llm(prompt)

    translation_messages.append(user_message)
    translation_messages.append(assistant_message)

    translations.append((speaker, translated_text))

    if i % THRESHOLD == 0 and i + KEEP <= total:
        print(f"[Generating summary after translation {i}]")
        saved_len = len(chat_history)
        _, sum_req, sum_res = summarize_messages()
        del chat_history[saved_len:]
        summary_messages.append(sum_req)
        summary_messages.append(sum_res)
        next_compression = i + KEEP

    if next_compression is not None and i == next_compression:
        print(f"[Compressing history after translation {i}: keeping {KEEP} pairs]")
        next_start = i + 1
        next_end = min(i + THRESHOLD + KEEP, total)
        terms_msgs = build_terms_messages(next_start, next_end)
        chat_history = (
            [system_message]
            + terms_msgs
            + summary_messages[-2:]
            + translation_messages[-KEEP * 2:]
        )
        next_compression = None

elapsed = time.time() - start_time

with open(args.output_file, "w", encoding="utf-8") as f:
    for speaker, translation in translations:
        f.write(f"{speaker}: {translation}\n")

print(f"\nTranslation complete: {FROM_LANG} → {TO_LANG} ({args.output_file})")
print(f"Processing time: {elapsed:.1f}s ({elapsed/60:.1f}min)")
