# 指定ファイルをローカルLLMで英語と日本語に翻訳（1行ずつ処理、文脈付き）

# デフォルトモデルは設定しない（指定必須）

import argparse

# メインパーサー
epilog_text = """
使用例:
  # 2段階翻訳の実行
  python translate.py phase1 input.txt -f French -t Spanish -o output.txt -m ollama:gemma3n:e4b
  python translate.py phase2a -o output.txt --draft-file output_draft.json -c ollama:qwen2.5:7b

  # 従来処理
  python translate.py legacy input.txt -f French -t Spanish -o output.txt -m ollama:gemma3n:e4b

詳細なヘルプ:
  python translate.py phase1 -h       # Phase 1のオプション
  python translate.py phase2a -h      # Phase 2a（統合品質チェック+修正）のオプション
  python translate.py legacy -h       # 従来処理のオプション
"""

parser = argparse.ArgumentParser(
    description="多段階翻訳システム",
    epilog=epilog_text,
    formatter_class=argparse.RawDescriptionHelpFormatter
)
subparsers = parser.add_subparsers(dest="command", help="実行するフェーズを選択")

# Phase 1: 初回翻訳
phase1_parser = subparsers.add_parser("phase1", help="初回翻訳を実行")
phase1_parser.add_argument("input_file", help="翻訳対象のテキストファイル")
phase1_parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: English, French, Japanese）")
phase1_parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: English, French, Japanese）")
phase1_parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
phase1_parser.add_argument("-m", "--model", required=True, help="翻訳モデル（例: ollama:gemma3n:e4b）")

# Phase 2a: 統合品質チェック+修正
phase2a_parser = subparsers.add_parser("phase2a", help="品質チェックと修正を統合実行")
phase2a_parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
phase2a_parser.add_argument("--draft-file", required=True, help="Phase 1で生成されたdraftファイル")
phase2a_parser.add_argument("-c", "--checker-model", required=True, help="品質チェック・修正用モデル（例: ollama:qwen2.5:7b）")

# Phase 2: 品質チェック（旧版、互換性維持）
phase2_parser = subparsers.add_parser("phase2", help="品質チェックを実行（旧版）")
phase2_parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
phase2_parser.add_argument("--draft-file", required=True, help="Phase 1で生成されたdraftファイル")
phase2_parser.add_argument("-c", "--checker-model", required=True, help="品質チェック用モデル（例: ollama:qwen2.5:7b）")

# Phase 3: 修正反映（旧版、互換性維持）
phase3_parser = subparsers.add_parser("phase3", help="修正反映を実行（旧版）")
phase3_parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
phase3_parser.add_argument("--draft-file", required=True, help="Phase 1で生成されたdraftファイル")
phase3_parser.add_argument("--check-file", required=True, help="Phase 2で生成されたcheckファイル")
phase3_parser.add_argument("-m", "--model", required=True, help="翻訳モデル（例: ollama:gemma3n:e4b）")

# 従来の統合処理（後方互換性）
legacy_parser = subparsers.add_parser("legacy", help="従来の統合処理（後方互換性）")
legacy_parser.add_argument("input_file", help="翻訳対象のテキストファイル")
legacy_parser.add_argument("-f", "--from", dest="from_lang", required=True, help="原語（例: English, French, Japanese）")
legacy_parser.add_argument("-t", "--to", dest="to_lang", required=True, help="翻訳先言語（例: English, French, Japanese）")
legacy_parser.add_argument("-o", "--output", dest="output_file", required=True, help="出力ファイル名")
legacy_parser.add_argument("-m", "--model", required=True, help="翻訳モデル（例: ollama:gemma3n:e4b）")
legacy_parser.add_argument("-r", "--reasoning-level", type=int, default=2, choices=[0, 1, 2], help="推論レベル: 0=推論なし, 1=標準推論, 2=2段階翻訳")

args = parser.parse_args()

# コマンドが指定されていない場合はヘルプを表示
if not args.command:
    parser.print_help()
    exit(1)

# サブコマンドに応じてphase設定
if args.command == "phase1":
    args.phase = 1
elif args.command == "phase2a":
    args.phase = "2a"
elif args.command == "phase2":
    args.phase = 2
elif args.command == "phase3":
    args.phase = 3
else:  # legacy
    args.phase = None

# Phase 1とlegacyの場合のみファイルを読み込み
if args.phase == 1 or args.command == "legacy":
    with open(args.input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
else:
    # Phase 2a/2/3ではJSONから処理するためlines不要
    lines = []

import json
import re
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt
from tqdm import tqdm

# 言語設定の取得（Phase 2/3用）
from_lang = getattr(args, 'from_lang', None)
to_lang = getattr(args, 'to_lang', None)

# フェーズベース処理またはレベル3の場合の分岐
if args.phase or (hasattr(args, 'reasoning_level') and args.reasoning_level == 3):
    # スキーマクラスは後で動的に作成する（メタデータ取得後）
    pass

# 従来のレベル別処理
elif hasattr(args, 'reasoning_level') and args.reasoning_level == 0:
    class Translation(BaseModel):
        translation: str = Field(description=f"{args.from_lang} to {args.to_lang} translation result")
elif hasattr(args, 'reasoning_level') and args.reasoning_level == 1:
    class Translation(BaseModel):
        reasoning: str = Field(description=f"Carefully analyze the meaning and context of the original {args.from_lang} text. Consider cultural nuances, idiomatic expressions, and the speaker's intent. Evaluate different possible translation choices and explain your reasoning for selecting the most appropriate words and phrasing for the {args.to_lang} translation.")
        translation: str = Field(description=f"{args.from_lang} to {args.to_lang} translation result")
elif hasattr(args, 'reasoning_level') and args.reasoning_level == 2:
    class Translation(BaseModel):
        draft_translation: str = Field(description=f"First draft translation from {args.from_lang} to {args.to_lang}")
        quality_check: str = Field(description=f"Analyze the draft translation for errors, mistranslations, language mixing, unnatural expressions, and cultural appropriateness. Check specifically that: 1) The text is completely translated into {args.to_lang}, 2) No {args.from_lang} words or expressions remain untranslated, 3) The translation is natural and appropriate. Identify specific issues and suggest improvements.")
        translation: str = Field(description=f"Final polished {args.from_lang} to {args.to_lang} translation based on the quality check feedback")

def normalize(text):
    # ord(ch)<32の文字をすべてスペースに変換
    normalized = ''.join(' ' if ord(ch) < 32 else ch for ch in text)
    # スペースの連続を1個にまとめる
    normalized = re.sub(r' +', ' ', normalized)
    return normalized.strip()

def load_phase_data(file_path):
    """フェーズ間データを読み込み"""
    if not file_path:
        return {}, []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'metadata' in data and 'results' in data:
                # resultsは常にリスト形式で返す
                return data['metadata'], data['results']
            else:
                # 旧形式との互換性
                return {}, data if isinstance(data, list) else []
    except FileNotFoundError:
        print(f"警告: ファイル {file_path} が見つかりません")
        return {}, []

def save_phase_data(data, file_path, metadata=None):
    """フェーズ間データを保存"""
    # dataが辞書の場合はリスト形式に変換
    if isinstance(data, dict):
        results_list = []
        for line_key, item_data in data.items():
            if isinstance(item_data, dict) and 'speaker' in item_data:
                results_list.append(item_data)
            else:
                # 古い形式の場合の互換性処理
                results_list.append(item_data)
        data = results_list
    
    output_data = {
        'metadata': metadata or {},
        'results': data
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

def get_phase_file_path(base_path, phase):
    """フェーズ別ファイルパスを生成"""
    base = base_path.rsplit('.', 1)[0]
    if phase == 1:
        return f"{base}_draft.json"
    elif phase == "2a":
        return f"{base}_final.json"
    elif phase == 2:
        return f"{base}_check.json"
    else:
        return base_path

# フェーズ別処理の準備
if args.phase or (hasattr(args, 'reasoning_level') and args.reasoning_level == 3):
    if args.phase == 1:
        # フェーズ1: 初回翻訳
        class DraftTranslation(BaseModel):
            translation: str = Field(description=f"Direct translation from {args.from_lang} to {args.to_lang}")
        
        current_schema = DraftTranslation
        current_model = args.model
        json_descriptions = create_json_descriptions_prompt(DraftTranslation)
    elif args.phase == "2a":
        # フェーズ2a: 統合品質チェック+修正
        draft_metadata, draft_data = load_phase_data(args.draft_file)
        # メタデータから言語設定を復元
        if 'from_lang' in draft_metadata:
            args.from_lang = draft_metadata['from_lang']
        if 'to_lang' in draft_metadata:
            args.to_lang = draft_metadata['to_lang']
        
        # 言語設定を取得後にスキーマを定義
        class QualityCheckAndRevision(BaseModel):
            quality_assessment: str = Field(description=f"Analyze this {args.from_lang} to {args.to_lang} translation for errors, mistranslations, language mixing, unnatural expressions, and cultural appropriateness. Check specifically that: 1) The text is completely translated into {args.to_lang}, 2) No {args.from_lang} words or expressions remain untranslated, 3) The translation is natural and appropriate. List specific issues found.")
            improvement_suggestions: str = Field(description=f"Provide specific suggestions for improving the translation quality")
            improved_translation: str = Field(description=f"Based on the quality assessment and improvement suggestions above, provide an improved {args.from_lang} to {args.to_lang} translation that addresses all identified issues")
        
        current_schema = QualityCheckAndRevision
        current_model = args.checker_model
        json_descriptions = create_json_descriptions_prompt(QualityCheckAndRevision)
    elif args.phase == 2:
        # フェーズ2: 品質チェック（旧版、互換性維持）
        draft_metadata, draft_data = load_phase_data(args.draft_file)
        # メタデータから言語設定を復元
        if 'from_lang' in draft_metadata:
            args.from_lang = draft_metadata['from_lang']
        if 'to_lang' in draft_metadata:
            args.to_lang = draft_metadata['to_lang']
        
        # 言語設定を取得後にスキーマを定義
        class QualityCheck(BaseModel):
            quality_assessment: str = Field(description=f"Analyze this {args.from_lang} to {args.to_lang} translation for errors, mistranslations, language mixing, unnatural expressions, and cultural appropriateness. Check specifically that: 1) The text is completely translated into {args.to_lang}, 2) No {args.from_lang} words or expressions remain untranslated, 3) The translation is natural and appropriate. List specific issues found.")
            improvement_suggestions: str = Field(description=f"Provide specific suggestions for improving the translation quality")
            needs_revision: bool = Field(description="True if the translation needs revision, False if it's acceptable as-is")
        
        current_schema = QualityCheck
        current_model = args.checker_model
        json_descriptions = create_json_descriptions_prompt(QualityCheck)
    elif args.phase == 3:
        # フェーズ3: 修正反映
        draft_metadata, draft_data = load_phase_data(args.draft_file)
        check_metadata, check_data = load_phase_data(args.check_file)
        # メタデータから言語設定を復元
        if 'from_lang' in draft_metadata:
            args.from_lang = draft_metadata['from_lang']
        if 'to_lang' in draft_metadata:
            args.to_lang = draft_metadata['to_lang']
        
        # 言語設定を取得後にスキーマを定義
        class RevisedTranslation(BaseModel):
            improved_translation: str = Field(description=f"Improved {args.from_lang} to {args.to_lang} translation incorporating the quality check feedback and suggestions")
        
        current_schema = RevisedTranslation
        current_model = args.model
        json_descriptions = create_json_descriptions_prompt(RevisedTranslation)
    else:
        # reasoning_level == 3: 自動3段階実行
        pass
else:
    # 従来処理
    current_schema = Translation
    current_model = args.model
    json_descriptions = create_json_descriptions_prompt(Translation)

context_history = []  # 文脈保持用

# 翻訳対象行を事前にカウント
translation_lines = [line for line in lines if line.strip() and ":" in line.strip()]

def create_phase_prompt(phase, speaker, text, line_key=None):
    """フェーズ別プロンプト作成"""
    if phase == 1 or (not args.phase and hasattr(args, 'reasoning_level') and args.reasoning_level != 3):
        # フェーズ1または従来処理: 翻訳
        return f"Translate the following {args.from_lang} text spoken by {speaker} into {args.to_lang}:\n{text}"
    elif phase == "2a":
        # フェーズ2a: 統合品質チェック+修正
        draft_translation = None
        original_text = None
        
        if isinstance(draft_data, dict) and line_key and line_key in draft_data:
            # 辞書形式
            draft_translation = draft_data[line_key]['translation']
            original_text = draft_data[line_key]['original']
        elif isinstance(draft_data, list):
            # リスト形式
            for item in draft_data:
                if isinstance(item, dict) and 'speaker' in item and 'original' in item:
                    if f"{item['speaker']}:{item['original']}" == line_key:
                        draft_translation = item['translation']
                        original_text = item['original']
                        break
        
        if draft_translation and original_text:
            return f"""Original {args.from_lang} text: {original_text}

Draft translation: {draft_translation}

Please analyze this translation for quality issues and provide an improved version. Pay special attention to:
1. Ensure no {args.from_lang} words or expressions remain untranslated
2. Check for mistranslations and unnatural expressions
3. Verify cultural appropriateness and context accuracy
4. Provide specific improvement suggestions
5. Generate a final improved translation that addresses all identified issues"""
        return f"No draft translation found for: {text}"
    elif phase == 2:
        # フェーズ2: 品質チェック（旧版、互換性維持）
        draft_translation = None
        original_text = None
        
        if isinstance(draft_data, dict) and line_key and line_key in draft_data:
            # 辞書形式
            draft_translation = draft_data[line_key]['translation']
            original_text = draft_data[line_key]['original']
        elif isinstance(draft_data, list):
            # リスト形式
            for item in draft_data:
                if isinstance(item, dict) and 'speaker' in item and 'original' in item:
                    if f"{item['speaker']}:{item['original']}" == line_key:
                        draft_translation = item['translation']
                        original_text = item['original']
                        break
        
        if draft_translation and original_text:
            return f"Original {args.from_lang} text: {original_text}\nDraft translation: {draft_translation}\n\nAnalyze this translation for quality issues."
        return f"No draft translation found for: {text}"
    elif phase == 3:
        # フェーズ3: 修正反映
        draft_translation = None
        original_text = None
        quality_assessment = None
        improvement_suggestions = None
        
        # draft_dataから検索（常にリスト形式）
        current_draft_idx = None
        for draft_idx, draft_item in enumerate(draft_data):
            if (isinstance(draft_item, dict) and 'speaker' in draft_item and 'original' in draft_item and
                f"{draft_item['speaker']}:{draft_item['original']}" == line_key):
                draft_translation = draft_item['translation']
                original_text = draft_item['original']
                current_draft_idx = draft_idx
                break
        
        # check_dataから検索（常にリスト形式、インデックスベース対応付け）
        if current_draft_idx is not None and current_draft_idx < len(check_data):
            check_item = check_data[current_draft_idx]
            if isinstance(check_item, dict):
                quality_assessment = check_item.get('quality_assessment')
                improvement_suggestions = check_item.get('improvement_suggestions')
        
        if draft_translation and original_text and quality_assessment:
            return f"""Original {args.from_lang} text: {original_text}

Draft translation: {draft_translation}

Quality assessment: {quality_assessment}

Improvement suggestions: {improvement_suggestions}

Based on the quality assessment and improvement suggestions above, please revise the draft translation. Pay special attention to:
1. Ensure no {args.from_lang} words or expressions remain untranslated
2. Replace unnatural expressions with natural {args.to_lang} phrasing
3. Improve vocabulary choices and expressions to fit the context
4. Address specific issues identified in the quality check

Provide the improved translation."""
        return f"No quality check data found for: {text}"

# フェーズデータ保存用
phase_results = {}

# フェーズ別処理
if args.phase in ["2a", 2, 3]:
    # Phase 2a/2/3: JSONデータから処理
    data_source = draft_data if args.phase in ["2a", 2] else draft_data
    
    # データ形式に応じて処理項目を生成
    processing_items = []
    if isinstance(data_source, dict):
        # 辞書形式（従来形式）
        processing_items = [(line_key, data['original'], data['speaker']) for line_key, data in data_source.items()]
    elif isinstance(data_source, list):
        # リスト形式（新形式）
        for data in data_source:
            if isinstance(data, dict) and 'speaker' in data and 'original' in data:
                line_key = f"{data['speaker']}:{data['original']}"
                processing_items.append((line_key, data['original'], data['speaker']))
else:
    # Phase 1/legacy: ファイルから処理
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

# 処理実行
for line_key, text, speaker in tqdm(processing_items, desc=f"フェーズ{args.phase or '統合'}処理"):
    print()
    print(f"{speaker}: {text}")
    
    # フェーズ別プロンプト作成
    prompt = create_phase_prompt(args.phase, speaker, text, line_key)
    
    # メッセージ配列準備
    messages = [prompt, json_descriptions]
    
    # フェーズ別コンテキスト追加（Phase 3以外）
    if args.phase not in [3] and context_history:
        context_lines = []
        context_lines.append("Previous conversation context:")
        context_lines.append("")
        for ctx in context_history[-5:]:
            context_lines.append(f"Original: {ctx['speaker']}: {ctx['original']}")
            context_lines.append(f"Translation: {ctx['speaker']}: {ctx['translation']}")
            context_lines.append("")
        context = "\n".join(context_lines)
        messages.insert(0, context)  # コンテキストを先頭に挿入
    
    # 実際の処理実行
    for j in range(5):
        if j:
            print("Retry:", j)
        try:
            result = generate_with_schema(
                messages,
                schema=current_schema,
                model=current_model,
                max_length=4096,
                show_params=True,
            )
            parsed = json.loads(result.text.strip())
            break
        except Exception as e:
            if j < 4:
                print(e)
            else:
                raise
    
    # フェーズ別結果処理
    if args.phase == 1:
        # フェーズ1: 翻訳結果を保存
        translated_text = normalize(parsed['translation'])
        phase_results[line_key] = {
            'original': text,
            'translation': translated_text,
            'speaker': speaker
        }
        context_history.append({
            'speaker': speaker,
            'original': text,
            'translation': translated_text
        })
    elif args.phase == "2a":
        # フェーズ2a: 統合品質チェック+修正結果を保存  
        translated_text = normalize(parsed['improved_translation'])
        phase_results[line_key] = {
            'original': text,
            'translation': translated_text,
            'speaker': speaker,
            'quality_assessment': parsed['quality_assessment'],
            'improvement_suggestions': parsed['improvement_suggestions']
        }
        context_history.append({
            'speaker': speaker,
            'original': text,
            'translation': translated_text
        })
    elif args.phase == 2:
        # フェーズ2: 品質チェック結果を保存（旧版、互換性維持）
        phase_results[line_key] = {
            'quality_assessment': parsed['quality_assessment'],
            'improvement_suggestions': parsed['improvement_suggestions'],
            'needs_revision': parsed['needs_revision']
        }
    elif args.phase == 3:
        # フェーズ3: 修正された翻訳を保存
        translated_text = normalize(parsed['improved_translation'])
        phase_results[line_key] = {'translation': translated_text}
        context_history.append({
            'speaker': speaker,
            'original': text,
            'translation': translated_text
        })
    else:
        # 従来処理
        if 'translation' in parsed:
            translated_text = normalize(parsed['translation'])
        elif 'draft_translation' in parsed:
            translated_text = normalize(parsed['translation'])
        else:
            translated_text = normalize(str(parsed))
        
        context_history.append({
            'speaker': speaker,
            'original': text,
            'translation': translated_text
        })

# 結果を保存
if args.phase:
    # フェーズ別結果をJSONで保存
    phase_file = get_phase_file_path(args.output_file, args.phase)
    
    # Phase 1ではメタデータも保存
    metadata = {}
    if args.phase == 1:
        metadata = {
            'from_lang': args.from_lang,
            'to_lang': args.to_lang,
            'input_file': args.input_file,
            'model': args.model
        }
    
    save_phase_data(phase_results, phase_file, metadata)
    print(f"フェーズ{args.phase}完了: {phase_file}")
    
    if args.phase in [1, "2a", 3]:
        # フェーズ1,2a,3は翻訳結果もテキストで出力
        with open(args.output_file, "w", encoding="utf-8") as f:
            for ctx in context_history:
                f.write(f"{ctx['speaker']}: {ctx['translation']}\n")
        print(f"翻訳結果: {args.output_file}")
else:
    # 従来処理: テキストファイルに保存
    with open(args.output_file, "w", encoding="utf-8") as f:
        for ctx in context_history:
            f.write(f"{ctx['speaker']}: {ctx['translation']}\n")
    print(f"翻訳完了: {args.from_lang} → {args.to_lang} ({args.output_file})")
