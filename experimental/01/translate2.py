# 3段階多モデル翻訳システム - 一気通貫実行版
# Phase 1 → Phase 2 → Phase 3 を自動的に順次実行

import argparse
import json
import re
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt
from tqdm import tqdm
import os

# コマンドライン引数の設定
parser = argparse.ArgumentParser(
    description="3段階多モデル翻訳システム（Phase 1→2→3自動実行）",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
使用例:
  python translate2.py input.txt -f French -t Spanish -o output.txt -m ollama:gemma3n:e4b -c ollama:qwen2.5:7b

  -m: Phase 1とPhase 3で使用する翻訳モデル
  -c: Phase 2で使用する品質チェック用モデル
"""
)

parser.add_argument("input_file", help="翻訳対象のテキストファイル")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: English, French, Japanese）")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: English, French, Japanese）")
parser.add_argument("-o", "--output", dest="output_file", required=True, help="最終出力ファイル名")
parser.add_argument("-m", "--model", required=True, help="翻訳モデル（Phase 1, 3で使用）")
parser.add_argument("-c", "--checker-model", required=True, help="品質チェック用モデル（Phase 2で使用）")
parser.add_argument("--draft-file", dest="draft_file", help="Phase 1の中間ファイルパス（デフォルト: [output]_draft.json）")
parser.add_argument("--check-file", dest="check_file", help="Phase 2の中間ファイルパス（デフォルト: [output]_check.json）")
parser.add_argument("--skip-existing", action="store_true", help="既存の中間ファイルがある場合は処理をスキップ")

args = parser.parse_args()

# 入力ファイル読み込み
with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

def normalize(text):
    """テキストの正規化"""
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()

def save_phase_data(data, file_path, metadata=None):
    """フェーズ間データをJSONで保存"""
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
    """翻訳のみをテキストファイルで保存"""
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
    """フェーズ間データをJSONから読み込み"""
    if not file_path or not os.path.exists(file_path):
        return {}, []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, dict) and 'metadata' in data and 'results' in data:
            return data['metadata'], data['results']
        else:
            return {}, data if isinstance(data, list) else []

def get_phase_file_path(base_path, phase):
    """フェーズ別ファイルパスを生成"""
    base = base_path.rsplit('.', 1)[0]
    if phase == 1:
        return f"{base}_draft.json"
    elif phase == 2:
        return f"{base}_check.json"
    else:
        return base_path

# 翻訳対象行を抽出
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

print(f"3段階翻訳を開始: {len(processing_items)}行を処理")

# ファイルパス設定
draft_file = args.draft_file if args.draft_file else get_phase_file_path(args.output_file, 1)
check_file = args.check_file if args.check_file else get_phase_file_path(args.output_file, 2)

# =============================================================================
# Phase 1: 初回翻訳
# =============================================================================
print("\n=== Phase 1: 初回翻訳 ===")

# 既存のdraft_fileがある場合はスキップするかチェック
if args.skip_existing and os.path.exists(draft_file):
    print(f"Phase 1をスキップ: 既存ファイル {draft_file} を使用")
    phase1_results = None  # 後で読み込む
else:

    class DraftTranslation(BaseModel):
        translation: str = Field(description=f"Direct translation from {args.from_lang} to {args.to_lang}")

    json_descriptions_phase1 = create_json_descriptions_prompt(DraftTranslation)
    phase1_results = {}
    context_history = []

    for line_key, text, speaker in tqdm(processing_items, desc="Phase 1"):
        prompt = f"Translate the following {args.from_lang} text spoken by {speaker} into {args.to_lang}:\n{text}"
        
        messages = [prompt, json_descriptions_phase1]
        
        # コンテキスト追加
        if context_history:
            context_lines = ["Previous conversation context:", ""]
            for ctx in context_history[-5:]:
                context_lines.append(f"Original: {ctx['speaker']}: {ctx['original']}")
                context_lines.append(f"Translation: {ctx['speaker']}: {ctx['translation']}")
                context_lines.append("")
            context = "\n".join(context_lines)
            messages.insert(0, context)
        
        # 翻訳実行
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

    # Phase 1結果を保存
    metadata = {
        'from_lang': args.from_lang,
        'to_lang': args.to_lang,
        'input_file': args.input_file,
        'model': args.model
    }
    save_phase_data(phase1_results, draft_file, metadata)
    
    # draft-fileのjson拡張子をtxtに変えて翻訳のみも保存
    draft_txt_file = draft_file.replace('.json', '.txt')
    save_translation_only(phase1_results, draft_txt_file)
    print(f"Phase 1完了: {draft_file}, {draft_txt_file}")

# =============================================================================
# Phase 2: 品質チェック
# =============================================================================
print("\n=== Phase 2: 品質チェック ===")

# 既存のcheck_fileがある場合はスキップするかチェック
if args.skip_existing and os.path.exists(check_file):
    print(f"Phase 2をスキップ: 既存ファイル {check_file} を使用")
else:

    class QualityCheck(BaseModel):
        quality_assessment: str = Field(description=f"Analyze this {args.from_lang} to {args.to_lang} translation for errors, mistranslations, language mixing, unnatural expressions, and cultural appropriateness. Check specifically that: 1) The text is completely translated into {args.to_lang}, 2) No {args.from_lang} words or expressions remain untranslated, 3) The translation is natural and appropriate. List specific issues found.")
        improvement_suggestions: str = Field(description=f"Provide specific suggestions for improving the translation quality")
        needs_revision: bool = Field(description="True if the translation needs revision, False if it's acceptable as-is")

    json_descriptions_phase2 = create_json_descriptions_prompt(QualityCheck)
    phase2_results = {}

    # Phase 1データを読み込み
    draft_metadata, draft_data = load_phase_data(draft_file)

    for line_key, text, speaker in tqdm(processing_items, desc="Phase 2"):
        # draft_dataから対応する翻訳を検索
        draft_translation = None
        original_text = None
        
        for item in draft_data:
            if isinstance(item, dict) and 'speaker' in item and 'original' in item:
                if f"{item['speaker']}:{item['original']}" == line_key:
                    draft_translation = item['translation']
                    original_text = item['original']
                    break
        
        if not draft_translation:
            print(f"警告: Phase 1の翻訳が見つかりません: {line_key}")
            continue
        
        prompt = f"Original {args.from_lang} text: {original_text}\nDraft translation: {draft_translation}\n\nAnalyze this translation for quality issues."
        
        messages = [prompt, json_descriptions_phase2]
        
        # 品質チェック実行
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

    # Phase 2結果を保存
    save_phase_data(phase2_results, check_file)
    print(f"Phase 2完了: {check_file}")

# =============================================================================
# Phase 3: 修正反映
# =============================================================================
print("\n=== Phase 3: 修正反映 ===")

class RevisedTranslation(BaseModel):
    improved_translation: str = Field(description=f"Improved {args.from_lang} to {args.to_lang} translation incorporating the quality check feedback and suggestions")

json_descriptions_phase3 = create_json_descriptions_prompt(RevisedTranslation)
phase3_results = {}
final_context_history = []

# Phase 1データとPhase 2データを読み込み
if phase1_results is None:  # Phase 1がスキップされた場合
    draft_metadata, draft_data = load_phase_data(draft_file)
check_metadata, check_data = load_phase_data(check_file)

for line_key, text, speaker in tqdm(processing_items, desc="Phase 3"):
    # draft_dataから対応する翻訳を検索
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
    
    # check_dataから対応する品質チェック結果を検索
    quality_assessment = None
    improvement_suggestions = None
    
    if current_draft_idx is not None and current_draft_idx < len(check_data):
        check_item = check_data[current_draft_idx]
        if isinstance(check_item, dict):
            quality_assessment = check_item.get('quality_assessment')
            improvement_suggestions = check_item.get('improvement_suggestions')
    
    if not (draft_translation and original_text and quality_assessment):
        print(f"警告: Phase 2の品質チェック結果が見つかりません: {line_key}")
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
    
    # 修正翻訳実行
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

print(f"Phase 3完了")

# 最終結果をテキストファイルに出力
with open(args.output_file, "w", encoding="utf-8") as f:
    for ctx in final_context_history:
        f.write(f"{ctx['speaker']}: {ctx['translation']}\n")

print(f"\n3段階翻訳完了: {args.from_lang} → {args.to_lang}")
print(f"最終結果: {args.output_file}")
draft_txt_file = draft_file.replace('.json', '.txt')
print(f"中間ファイル: {draft_file}, {draft_txt_file}, {check_file}")