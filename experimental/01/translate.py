# Translate the specified file into English and Japanese using a local LLM (processed line by line, with context)

import argparse
parser = argparse.ArgumentParser(description="Translate dialogue text 1:1")
parser.add_argument("input_file", help="Text file to translate")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="Source language (e.g. English, French, Japanese)")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="Target language (e.g. English, French, Japanese)")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="Output file name")
parser.add_argument("-m", "--model", required=True, help="Model to use for translation")
parser.add_argument("-r", "--reasoning-level", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Reasoning level: 0=no reasoning, 1=standard reasoning, 2=two-stage translation, 3=three-stage translation, 4=split three-stage translation")
parser.add_argument("--history", type=int, default=5, help="Number of past dialogue turns to include in context (default: 5)")
parser.add_argument("--translated-context", action="store_true", help="Provide only translated text in the history context (instead of the bilingual format)")
parser.add_argument("--no-think", action="store_true", help="Disable thinking processing (for Qwen3 models)")
args = parser.parse_args()

with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

import json
import re
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt
from tqdm import tqdm

# Field templates
translation_field = Field(description=f"Direct translation from {args.from_lang} to {args.to_lang}")
translation_result_field = Field(description=f"{args.from_lang} to {args.to_lang} translation result")
reasoning_field = Field(description=f"Detailed translation reasoning process:\n1. Syntactic analysis of the original {args.from_lang} text (subject, predicate, object, modifiers, etc.)\n2. Contextual interpretation of speaker's intent and emotional tone\n3. Evaluation of translation options for key vocabulary and idiomatic expressions\n4. Consideration of cultural nuances and appropriate register/politeness level\n5. Justification for final translation choices and overall approach")
draft_translation_field = Field(description=f"First draft translation from {args.from_lang} to {args.to_lang}")
quality_assessment_field = Field(description=f"Analyze this {args.from_lang} to {args.to_lang} translation for errors, mistranslations, language mixing, unnatural expressions, and cultural appropriateness. Check specifically that: 1) The text is completely translated into {args.to_lang}, 2) No {args.from_lang} words or expressions remain untranslated, 3) There are no omissions of information from the original text or additions of information not present in the original, 4) The translation is natural and appropriate. List specific issues found.")
improvement_suggestions_field = Field(description=f"Provide specific suggestions for improving the translation quality")
improved_translation_field = Field(description=f"Based on the quality assessment and improvement suggestions above, provide an improved {args.from_lang} to {args.to_lang} translation that addresses all identified issues")

if args.reasoning_level == 0:
    class Translation(BaseModel):
        translation: str = translation_field
elif args.reasoning_level == 1:
    class Translation(BaseModel):
        reasoning: str = reasoning_field
        translation: str = translation_result_field
elif args.reasoning_level == 2:
    class Translation(BaseModel):
        draft_translation: str = draft_translation_field
        quality_assessment: str = quality_assessment_field
        improvement_suggestions: str = improvement_suggestions_field
        improved_translation: str = improved_translation_field
elif args.reasoning_level == 3:
    class Translation(BaseModel):
        reasoning: str = reasoning_field
        draft_translation: str = draft_translation_field
        quality_assessment: str = quality_assessment_field
        improvement_suggestions: str = improvement_suggestions_field
        improved_translation: str = improved_translation_field
elif args.reasoning_level == 4:
    # Stage 1: reasoning and initial translation
    class FirstStageTranslation(BaseModel):
        reasoning: str = reasoning_field
        draft_translation: str = draft_translation_field

    # Stage 2: quality assessment and improved translation
    class SecondStageTranslation(BaseModel):
        quality_assessment: str = quality_assessment_field
        improvement_suggestions: str = improvement_suggestions_field
        improved_translation: str = improved_translation_field

    Translation = FirstStageTranslation  # Default is stage 1

json_descriptions = create_json_descriptions_prompt(Translation)

def normalize(text):
    # Convert all characters with ord(ch)<32 to spaces
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    # Collapse consecutive spaces into one
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()

def generate_with_retry(prompts, schema, model, stage_name=""):
    """LLM generation function with retry capability"""
    descriptions = create_json_descriptions_prompt(schema)
    for j in range(5):
        if j:
            print(f"Retry{' (' + stage_name + ')' if stage_name else ''}:", j)
        try:
            result = generate_with_schema(
                prompts + [descriptions],
                schema=schema,
                model=model,
                max_length=8192*2,
                show_params=False,
                include_thoughts=(not args.no_think),
            )
            return json.loads(result.text.strip())
        except Exception as e:
            if j < 4:
                print(e)
            else:
                raise

context_history = []  # for keeping context

# Count the lines to translate in advance
translation_lines = [line for line in lines if line.strip() and ":" in line.strip()]

# Translate line by line
for i, line in enumerate(tqdm(lines, desc="Translating")):
    line = line.strip()

    # Skip if the speaker cannot be separated
    if ":" not in line:
        continue

    print()
    print(line)

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
            if args.translated_context:
                # Provide only the translated text
                context_lines.append(f"{ctx['speaker']}: {ctx['translation']}")
            else:
                # Provide in bilingual format (default)
                context_lines.append(f"Original: {ctx['speaker']}: {ctx['original']}")
                context_lines.append(f"Translation: {ctx['speaker']}: {ctx['translation']}")
                context_lines.append("")

    context = "\n".join(context_lines) if context_lines else "(No context)"

    # Create the prompt (including speaker information)
    prompt = f"Translate the following {args.from_lang} text spoken by {speaker} into {args.to_lang}:\n{text}"

    # Run the actual translation
    if args.reasoning_level == 4:
        # Level 4: processing split into two stages
        # Stage 1: reasoning and initial translation
        first_parsed = generate_with_retry([context, prompt], FirstStageTranslation, args.model, "Stage 1")

        # Stage 2: quality assessment and improved translation
        second_stage_prompt = f"Review and improve this {args.from_lang} to {args.to_lang} translation:\n\nOriginal: {text}\nDraft translation: {first_parsed['draft_translation']}"
        second_parsed = generate_with_retry([context, second_stage_prompt], SecondStageTranslation, args.model, "Stage 2")

        # Merge the results
        parsed = {
            'reasoning': first_parsed['reasoning'],
            'draft_translation': first_parsed['draft_translation'],
            'quality_assessment': second_parsed['quality_assessment'],
            'improvement_suggestions': second_parsed['improvement_suggestions'],
            'improved_translation': second_parsed['improved_translation']
        }
    else:
        # Legacy single-call processing
        parsed = generate_with_retry([context, prompt], Translation, args.model)

    # Add to context history
    if args.reasoning_level in [2, 3, 4]:
        translated_text = normalize(parsed['improved_translation'])
    else:
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
