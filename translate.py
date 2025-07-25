# 指定ファイルをローカルLLMで英語と日本語に翻訳（1行ずつ処理、文脈付き）

import argparse

DEFAULT_MODEL = "ollama:gemma3n:e4b"

parser = argparse.ArgumentParser(description="フランス語対話テキストを英語と日本語に翻訳")
parser.add_argument("input_file", help="翻訳対象のフランス語テキストファイル")
parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"翻訳に使用するモデル（デフォルト: {DEFAULT_MODEL}）")
parser.add_argument("--test", action="store_true", help="dry-runモード（実際の翻訳は行わない）")
args = parser.parse_args()

import json
from pathlib import Path
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt

class Translation(BaseModel):
    reasoning: str = Field(description="翻訳前の検討")
    translation: str = Field(description="翻訳")

class Translations(BaseModel):
    french: Translation = Field(description="フランス語翻訳")
    japanese: Translation = Field(description="日本語翻訳")

# fr-onde.txtを読み込み
with open(args.input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

def make_output_filename(lang):
    base = Path(args.input_file)
    stem = base.stem.removesuffix("-en")
    return str(base.with_name(f"{stem}-{lang}.txt"))

output_fr = make_output_filename("fr")
output_ja = make_output_filename("ja")

json_descriptions = create_json_descriptions_prompt(Translations)

# 翻訳結果を保存するリスト
french_lines = []
japanese_lines = []
# 文脈保持用
context_history = []

# 1行ずつ翻訳
for i, line in enumerate(lines):
    line = line.strip()
    if line and ":" in line:
        speaker, text = line.split(":", 1)
        speaker = speaker.strip()
        text = text.strip()
        
        # 文脈作成（直前の5つの翻訳結果）
        context_lines = []
        if context_history:
            context_lines.append("ここまでの会話の流れ:")
            context_lines.append("")
            for ctx in context_history[-5:]:
                context_lines.append(f"原文: {ctx['speaker']}: {ctx['french']}")
                context_lines.append(f"フランス語: {ctx['speaker']}: {ctx['french']}")
                context_lines.append(f"日本語: {ctx['speaker']}: {ctx['japanese']}")
                context_lines.append("")
        
        context = "\n".join(context_lines) if context_lines else "（文脈なし）"
        
        # プロンプト作成（話者情報を含める）
        prompt = f"話者{speaker}の以下の英語の発言をフランス語と日本語に翻訳してください：\n{text}"
        
        if args.test:
            # dry-runモード：実際の翻訳は行わず、ダミーデータを使用
            print(f"[TEST] Context:\n{context}")
            print(f"[TEST] Prompt:\n{prompt}")

            french_text = f"[TEST FRENCH] {text}"
            japanese_text = f"[TEST JAPANESE] {text}"
        else:
            # 実際の翻訳実行
            result = generate_with_schema(
                [context, prompt, json_descriptions],
                schema=Translations,
                model=args.model,
            )
            
            if result and result.text:
                try:
                    parsed = json.loads(result.text.strip())
                    french_text = parsed['french']['translation']
                    japanese_text = parsed['japanese']['translation']
                except json.JSONDecodeError:
                    # JSON解析失敗時は原文を保持
                    french_text = text
                    japanese_text = text
            else:
                # 翻訳失敗時は原文を保持
                french_text = text
                japanese_text = text

        french_lines.append(f"{speaker}: {french_text}")
        japanese_lines.append(f"{speaker}: {japanese_text}")
        
        # 文脈履歴に追加
        context_history.append({
            'speaker': speaker,
            'french': text,
            'french': french_text,
            'japanese': japanese_text
        })
        
        if not args.test:
            print(f"翻訳完了: {i+1}/{len([l for l in lines if l.strip() and ':' in l])} - {speaker}")
    else:
        # 空行はそのまま保持
        french_lines.append("")
        japanese_lines.append("")

# 結果を保存
with open(output_fr, "w", encoding="utf-8") as f:
    for line in french_lines:
        f.write(line + "\n")

with open(output_ja, "w", encoding="utf-8") as f:
    for line in japanese_lines:
        f.write(line + "\n")

if args.test:
    print(f"[TEST] 処理完了: {len([l for l in lines if l.strip() and ':' in l])}行をテスト処理")
    print("[TEST] 実際のファイルは生成されませんでした")
else:
    print(f"翻訳完了: フランス語版 {output_fr}、日本語版 {output_ja} を生成")
