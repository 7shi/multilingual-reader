# Translate the specified file using a local LLM (free-form reasoning test)

import argparse
parser = argparse.ArgumentParser(description="Translate dialogue text 1:1 (free-form reasoning test)")
parser.add_argument("input_file", help="Text file to translate")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="Source language (e.g. English, French, Japanese)")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="Target language (e.g. English, French, Japanese)")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="Output file name")
parser.add_argument("-m", "--model", required=True, help="Model to use for translation")
parser.add_argument("--history", type=int, default=5, help="Number of past dialogue turns to include in context (default: 5)")
parser.add_argument("--no-think", action="store_true", help="Disable reasoning processing (for Qwen3 models)")
args = parser.parse_args()

with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

import re
from llm7shi.compat import generate_with_schema
from llm7shi import bold
from tqdm import tqdm

def normalize(text):
    # Convert all characters with ord(ch)<32 to spaces
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    # Collapse consecutive spaces into one
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()


def generate_with_retry(system_prompt, prompts, model):
    """LLM generation function with retry capability"""
    for j in range(5):
        if j:
            print(f"Retry: {j}")
        try:
            result = generate_with_schema(
                prompts,
                system_prompt=system_prompt,
                model=model,
                max_length=4096,
                show_params=False,
                include_thoughts=(not args.no_think),
            )
            return result.text.strip()
        except Exception as e:
            if j < 4:
                print(e)
            else:
                raise

context_history = []  # for keeping context

# Extract the lines to translate in advance
translation_lines = [l for line in lines if (l := line.strip()) and ":" in l]

# Translate line by line
for line in tqdm(translation_lines, desc="Translating"):
    print("\n\n" + bold(f"[{args.from_lang}]"), line + "\n")

    # Separate the speaker
    speaker, text = line.split(":", 1)
    speaker = speaker.strip()
    text = text.strip()

    # Build context (translation results from the last `history` turns)
    context_lines = []
    if context_history and args.history > 0:
        context_lines.append("Previous conversation context:")
        context_lines.append("")
        for ctx in context_history[-args.history:]:
            # Provide in bilingual format
            context_lines.append(f"Original: {ctx['speaker']}: {ctx['original']}")
            context_lines.append(f"Translation: {ctx['speaker']}: {ctx['translation']}")
            context_lines.append("")

    context = "\n".join(context_lines) if context_lines else "(No context)"

    # Create the system prompt and user prompt (always in reasoning mode)
    system_prompt = f"""You are a professional translator. Please translate {args.from_lang} to {args.to_lang}.

First, briefly analyze the text for:
1. Key vocabulary and expressions
2. Speaker's intent and tone
3. Cultural context and appropriate register

Then provide your final translation on the last line."""
    prompt = f"Analyze and translate the following {args.from_lang} text into {args.to_lang}:\n{line}"

    # Run translation
    output_text = generate_with_retry(system_prompt, [context, prompt], args.model)

    # Extract the translation result (always in reasoning mode, so extraction is always run)
    print("\n" + bold(f"[{args.to_lang}]"), end=" ")
    extraction_system_prompt = "Output only the requested translation text."
    extraction_prompt = f"Extract only the final {args.to_lang} translation from the following text. Look for the actual translation result, not the reasoning or analysis sections. Output only the {args.to_lang} translation without any explanations, alternatives, or formatting in any language. If the entire translation is wrapped in quotation marks, remove only the outer quotation marks:\n\n{output_text}"

    # Run extraction
    translated_text = generate_with_retry(extraction_system_prompt, [extraction_prompt], args.model)
    translated_text = normalize(translated_text).removeprefix(speaker + ":").strip()
    print()

    # Add to context history
    context_history.append({
        'speaker': speaker,
        'original': text,
        'translation': translated_text
    })

# Save results
with open(args.output_file, "w", encoding="utf-8") as f:
    for ctx in context_history:
        f.write(f"{ctx['speaker']}: {ctx['translation']}\n")

print(f"Translation complete: {args.from_lang} → {args.to_lang} ({args.output_file})")
