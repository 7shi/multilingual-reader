# Translate the given file into English and Japanese using a local LLM (line by line, with context)

DEFAULT_MODEL = "ollama:gemma3n:e4b"

import argparse
parser = argparse.ArgumentParser(description="Translate dialogue text line by line")
parser.add_argument("input_file", help="Text file to translate")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="Source language (e.g. English, French, Japanese)")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="Target language (e.g. English, French, Japanese)")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="Output file name")
parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"Model to use for translation (default: {DEFAULT_MODEL})")
parser.add_argument("-r", "--reasoning-level", type=int, default=2, choices=[0, 1, 2], help="Reasoning level: 0=no reasoning, 1=standard reasoning, 2=two-stage translation")
args = parser.parse_args()

with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

import json
import re
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt
from tqdm import tqdm

if args.reasoning_level == 0:
    class Translation(BaseModel):
        translation: str = Field(description=f"{args.from_lang} to {args.to_lang} translation result")
elif args.reasoning_level == 1:
    class Translation(BaseModel):
        reasoning: str = Field(description=f"Carefully analyze the meaning and context of the original {args.from_lang} text. Consider cultural nuances, idiomatic expressions, and the speaker's intent. Evaluate different possible translation choices and explain your reasoning for selecting the most appropriate words and phrasing for the {args.to_lang} translation.")
        translation: str = Field(description=f"{args.from_lang} to {args.to_lang} translation result")
elif args.reasoning_level == 2:
    class Translation(BaseModel):
        draft_translation: str = Field(description=f"First draft translation from {args.from_lang} to {args.to_lang}")
        quality_check: str = Field(description=f"Analyze the draft translation for errors, mistranslations, language mixing, unnatural expressions, and cultural appropriateness. Identify specific issues and suggest improvements.")
        translation: str = Field(description=f"Final polished {args.from_lang} to {args.to_lang} translation based on the quality check feedback")

json_descriptions = create_json_descriptions_prompt(Translation)

def normalize(text):
    # Convert all characters with ord(ch)<32 to spaces
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    # Collapse consecutive spaces into one
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()

context_history = []  # for keeping context

# Count translation-target lines in advance
translation_lines = [line for line in lines if line.strip() and ":" in line.strip()]

# Translate line by line
for i, line in enumerate(tqdm(lines, desc="Translating")):
    line = line.strip()

    # Skip if the speaker can't be separated
    if ":" not in line:
        continue

    print()
    print(line)

    # Separate speaker
    speaker, text = line.split(":", 1)
    speaker = speaker.strip()
    text = text.strip()

    # Build context (the last 5 translation results)
    context_lines = []
    if context_history:
        context_lines.append("Previous conversation context:")
        context_lines.append("")
        for ctx in context_history[-5:]:
            context_lines.append(f"Original: {ctx['speaker']}: {ctx['original']}")
            context_lines.append(f"Translation: {ctx['speaker']}: {ctx['translation']}")
            context_lines.append("")

    context = "\n".join(context_lines) if context_lines else "(No context)"

    # Build prompt (include speaker info)
    prompt = f"Translate the following {args.from_lang} text spoken by {speaker} into {args.to_lang}:\n{text}"

    # Run the actual translation
    for j in range(5):
        if j:
            print("Retry:", j)
        try:
            result = generate_with_schema(
                [context, prompt, json_descriptions],
                schema=Translation,
                model=args.model,
                max_length=4096,
                show_params=False,
            )
            parsed = json.loads(result.text.strip())
            break
        except Exception as e:
            if j < 4:
                print(e)
            else:
                raise

    # Add to context history
    translated_text = normalize(parsed['translation'])
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
