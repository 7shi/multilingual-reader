# Three-stage multi-model translation system - end-to-end execution version
# Automatically runs Phase 1 -> Phase 2 -> Phase 3 in sequence

import argparse
import json
import re
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt
from tqdm import tqdm
import os

# Command-line argument setup
parser = argparse.ArgumentParser(
    description="Three-stage multi-model translation system (automatic Phase 1->2->3 execution)",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Example:
  python translate2.py input.txt -f French -t Spanish -o output.txt -m ollama:gemma3n:e4b -c ollama:qwen2.5:7b

  -m: translation model used in Phase 1 and Phase 3
  -c: quality-check model used in Phase 2
"""
)

parser.add_argument("input_file", help="Text file to translate")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="Source language (e.g. English, French, Japanese)")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="Target language (e.g. English, French, Japanese)")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="Final output file name")
parser.add_argument("-m", "--model", required=True, help="Translation model (used in Phase 1, 3)")
parser.add_argument("-c", "--checker-model", required=True, help="Quality-check model (used in Phase 2)")
parser.add_argument("--draft-file", dest="draft_file", help="Phase 1 intermediate file path (default: [output]_draft.json)")
parser.add_argument("--check-file", dest="check_file", help="Phase 2 intermediate file path (default: [output]_check.json)")
parser.add_argument("--skip-existing", action="store_true", help="Skip processing if intermediate files already exist")

args = parser.parse_args()

# Read the input file
with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

def normalize(text):
    """Normalize text"""
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()

def save_phase_data(data, file_path, metadata=None):
    """Save inter-phase data as JSON"""
    if isinstance(data, dict):
        results_list = []
        for line_key, item_data in data.items():
            if isinstance(item_data, dict) and 'speaker' in item_data:
                results_list.append(item_data)
            else:
                results_list.append(item_data)
        data = results_list
    
    output_data = {
        'metadata': metadata or {},
        'results': data
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

def save_translation_only(data, file_path):
    """Save only the translations as a text file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        if isinstance(data, dict):
            for line_key, item_data in data.items():
                if isinstance(item_data, dict) and 'speaker' in item_data and 'translation' in item_data:
                    f.write(f"{item_data['speaker']}: {item_data['translation']}\n")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and 'speaker' in item and 'translation' in item:
                    f.write(f"{item['speaker']}: {item['translation']}\n")

def load_phase_data(file_path):
    """Load inter-phase data from JSON"""
    if not file_path or not os.path.exists(file_path):
        return {}, []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, dict) and 'metadata' in data and 'results' in data:
            return data['metadata'], data['results']
        else:
            return {}, data if isinstance(data, list) else []

def get_phase_file_path(base_path, phase):
    """Generate the file path for each phase"""
    base = base_path.rsplit('.', 1)[0]
    if phase == 1:
        return f"{base}_draft.json"
    elif phase == 2:
        return f"{base}_check.json"
    else:
        return base_path

# Extract the lines to translate
processing_items = []
for line in lines:
    line = line.strip()
    if ":" not in line:
        continue
    speaker, text = line.split(":", 1)
    speaker = speaker.strip()
    text = text.strip()
    line_key = f"{speaker}:{text}"
    processing_items.append((line_key, text, speaker))

print(f"Starting three-stage translation: processing {len(processing_items)} lines")

# File path setup
draft_file = args.draft_file if args.draft_file else get_phase_file_path(args.output_file, 1)
check_file = args.check_file if args.check_file else get_phase_file_path(args.output_file, 2)

# =============================================================================
# Phase 1: initial translation
# =============================================================================
print("\n=== Phase 1: initial translation ===")

# Check whether to skip based on an existing draft_file
if args.skip_existing and os.path.exists(draft_file):
    print(f"Skipping Phase 1: using existing file {draft_file}")
    phase1_results = None  # loaded later
else:

    class DraftTranslation(BaseModel):
        translation: str = Field(description=f"Direct translation from {args.from_lang} to {args.to_lang}")

    json_descriptions_phase1 = create_json_descriptions_prompt(DraftTranslation)
    phase1_results = {}
    context_history = []

    for line_key, text, speaker in tqdm(processing_items, desc="Phase 1"):
        prompt = f"Translate the following {args.from_lang} text spoken by {speaker} into {args.to_lang}:\n{text}"

        messages = [prompt, json_descriptions_phase1]

        # Add context
        if context_history:
            context_lines = ["Previous conversation context:", ""]
            for ctx in context_history[-5:]:
                context_lines.append(f"Original: {ctx['speaker']}: {ctx['original']}")
                context_lines.append(f"Translation: {ctx['speaker']}: {ctx['translation']}")
                context_lines.append("")
            context = "\n".join(context_lines)
            messages.insert(0, context)

        # Run translation
        for j in range(5):
            try:
                result = generate_with_schema(
                    messages,
                    schema=DraftTranslation,
                    model=args.model,
                    max_length=4096,
                    show_params=(j == 0),
                )
                parsed = json.loads(result.text.strip())
                break
            except Exception as e:
                if j < 4:
                    print(f"Retry {j+1}: {e}")
                else:
                    raise

        translated_text = normalize(parsed['translation'])
        phase1_results[line_key] = {
            'original': text,
            'translation': translated_text,
            'speaker': speaker
        }
        context_history.append({
            'speaker': speaker,
            'original': text,
            'translation': translated_text
        })

    # Save Phase 1 results
    metadata = {
        'from_lang': args.from_lang,
        'to_lang': args.to_lang,
        'input_file': args.input_file,
        'model': args.model
    }
    save_phase_data(phase1_results, draft_file, metadata)

    # Also save translations only, with the draft file's json extension changed to txt
    draft_txt_file = draft_file.replace('.json', '.txt')
    save_translation_only(phase1_results, draft_txt_file)
    print(f"Phase 1 complete: {draft_file}, {draft_txt_file}")

# =============================================================================
# Phase 2: quality check
# =============================================================================
print("\n=== Phase 2: quality check ===")

# Check whether to skip based on an existing check_file
if args.skip_existing and os.path.exists(check_file):
    print(f"Skipping Phase 2: using existing file {check_file}")
else:

    class QualityCheck(BaseModel):
        quality_assessment: str = Field(description=f"Analyze this {args.from_lang} to {args.to_lang} translation for errors, mistranslations, language mixing, unnatural expressions, and cultural appropriateness. Check specifically that: 1) The text is completely translated into {args.to_lang}, 2) No {args.from_lang} words or expressions remain untranslated, 3) The translation is natural and appropriate. List specific issues found.")
        improvement_suggestions: str = Field(description=f"Provide specific suggestions for improving the translation quality")
        needs_revision: bool = Field(description="True if the translation needs revision, False if it's acceptable as-is")

    json_descriptions_phase2 = create_json_descriptions_prompt(QualityCheck)
    phase2_results = {}

    # Load Phase 1 data
    draft_metadata, draft_data = load_phase_data(draft_file)

    for line_key, text, speaker in tqdm(processing_items, desc="Phase 2"):
        # Search draft_data for the corresponding translation
        draft_translation = None
        original_text = None

        for item in draft_data:
            if isinstance(item, dict) and 'speaker' in item and 'original' in item:
                if f"{item['speaker']}:{item['original']}" == line_key:
                    draft_translation = item['translation']
                    original_text = item['original']
                    break

        if not draft_translation:
            print(f"Warning: Phase 1 translation not found: {line_key}")
            continue

        prompt = f"Original {args.from_lang} text: {original_text}\nDraft translation: {draft_translation}\n\nAnalyze this translation for quality issues."

        messages = [prompt, json_descriptions_phase2]

        # Run quality check
        for j in range(5):
            try:
                result = generate_with_schema(
                    messages,
                    schema=QualityCheck,
                    model=args.checker_model,
                    max_length=4096,
                    show_params=(j == 0),
                )
                parsed = json.loads(result.text.strip())
                break
            except Exception as e:
                if j < 4:
                    print(f"Retry {j+1}: {e}")
                else:
                    raise

        phase2_results[line_key] = {
            'quality_assessment': parsed['quality_assessment'],
            'improvement_suggestions': parsed['improvement_suggestions'],
            'needs_revision': parsed['needs_revision']
        }

    # Save Phase 2 results
    save_phase_data(phase2_results, check_file)
    print(f"Phase 2 complete: {check_file}")

# =============================================================================
# Phase 3: apply revisions
# =============================================================================
print("\n=== Phase 3: apply revisions ===")

class RevisedTranslation(BaseModel):
    improved_translation: str = Field(description=f"Improved {args.from_lang} to {args.to_lang} translation incorporating the quality check feedback and suggestions")

json_descriptions_phase3 = create_json_descriptions_prompt(RevisedTranslation)
phase3_results = {}
final_context_history = []

# Load Phase 1 and Phase 2 data
if phase1_results is None:  # If Phase 1 was skipped
    draft_metadata, draft_data = load_phase_data(draft_file)
check_metadata, check_data = load_phase_data(check_file)

for line_key, text, speaker in tqdm(processing_items, desc="Phase 3"):
    # Search draft_data for the corresponding translation
    draft_translation = None
    original_text = None
    current_draft_idx = None

    for draft_idx, draft_item in enumerate(draft_data):
        if (isinstance(draft_item, dict) and 'speaker' in draft_item and 'original' in draft_item and
            f"{draft_item['speaker']}:{draft_item['original']}" == line_key):
            draft_translation = draft_item['translation']
            original_text = draft_item['original']
            current_draft_idx = draft_idx
            break

    # Search check_data for the corresponding quality-check result
    quality_assessment = None
    improvement_suggestions = None

    if current_draft_idx is not None and current_draft_idx < len(check_data):
        check_item = check_data[current_draft_idx]
        if isinstance(check_item, dict):
            quality_assessment = check_item.get('quality_assessment')
            improvement_suggestions = check_item.get('improvement_suggestions')

    if not (draft_translation and original_text and quality_assessment):
        print(f"Warning: Phase 2 quality-check result not found: {line_key}")
        continue
    
    prompt = f"""Original {args.from_lang} text: {original_text}

Draft translation: {draft_translation}

Quality assessment: {quality_assessment}

Improvement suggestions: {improvement_suggestions}

Based on the quality assessment and improvement suggestions above, please revise the draft translation. Pay special attention to:
1. Ensure no {args.from_lang} words or expressions remain untranslated
2. Replace unnatural expressions with natural {args.to_lang} phrasing
3. Improve vocabulary choices and expressions to fit the context
4. Address specific issues identified in the quality check

Provide the improved translation."""
    
    messages = [prompt, json_descriptions_phase3]

    # Run revised translation
    for j in range(5):
        try:
            result = generate_with_schema(
                messages,
                schema=RevisedTranslation,
                model=args.model,
                max_length=4096,
                show_params=(j == 0),
            )
            parsed = json.loads(result.text.strip())
            break
        except Exception as e:
            if j < 4:
                print(f"Retry {j+1}: {e}")
            else:
                raise

    translated_text = normalize(parsed['improved_translation'])
    phase3_results[line_key] = {'translation': translated_text}
    final_context_history.append({
        'speaker': speaker,
        'original': text,
        'translation': translated_text
    })

print(f"Phase 3 complete")

# Write the final result to a text file
with open(args.output_file, "w", encoding="utf-8") as f:
    for ctx in final_context_history:
        f.write(f"{ctx['speaker']}: {ctx['translation']}\n")

print(f"\nThree-stage translation complete: {args.from_lang} → {args.to_lang}")
print(f"Final result: {args.output_file}")
draft_txt_file = draft_file.replace('.json', '.txt')
print(f"Intermediate files: {draft_file}, {draft_txt_file}, {check_file}")