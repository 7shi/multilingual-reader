# fr-onde.txtをローカルLLMで英語と日本語に翻訳（1行ずつ処理、文脈付き）
import argparse
import json
from pydantic import BaseModel, Field
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt

parser = argparse.ArgumentParser(description="フランス語対話テキストを英語と日本語に翻訳")
parser.add_argument("--test", action="store_true", help="dry-runモード（実際の翻訳は行わない）")
args = parser.parse_args()

model = "ollama:gemma3n:e4b"

class Translation(BaseModel):
    english: str = Field(description="英語翻訳")
    japanese: str = Field(description="日本語翻訳")

# fr-onde.txtを読み込み
with open("fr-onde.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

json_descriptions = create_json_descriptions_prompt(Translation)

# 翻訳結果を保存するリスト
english_lines = []
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
                context_lines.append(f"英語: {ctx['speaker']}: {ctx['english']}")
                context_lines.append(f"日本語: {ctx['speaker']}: {ctx['japanese']}")
                context_lines.append("")
        
        context = "\n".join(context_lines) if context_lines else "（文脈なし）"
        
        # プロンプト作成（話者情報を含める）
        prompt = f"話者{speaker}の以下のフランス語の発言を英語と日本語に翻訳してください：\n{text}"
        
        if args.test:
            # dry-runモード：実際の翻訳は行わず、ダミーデータを使用
            print(f"[TEST] Context:\n{context}")
            print(f"[TEST] Prompt:\n{prompt}")
            
            english_text = f"[TEST ENGLISH] {text}"
            japanese_text = f"[TEST JAPANESE] {text}"
        else:
            # 実際の翻訳実行
            result = generate_with_schema(
                [context, prompt, json_descriptions],
                schema=Translation,
                model=model,
            )
            
            if result and result.text:
                try:
                    parsed = json.loads(result.text.strip())
                    english_text = parsed.get('english', text)
                    japanese_text = parsed.get('japanese', text)
                except json.JSONDecodeError:
                    # JSON解析失敗時は原文を保持
                    english_text = text
                    japanese_text = text
            else:
                # 翻訳失敗時は原文を保持
                english_text = text
                japanese_text = text
        
        english_lines.append(f"{speaker}: {english_text}")
        japanese_lines.append(f"{speaker}: {japanese_text}")
        
        # 文脈履歴に追加
        context_history.append({
            'speaker': speaker,
            'french': text,
            'english': english_text,
            'japanese': japanese_text
        })
        
        if not args.test:
            print(f"翻訳完了: {i+1}/{len([l for l in lines if l.strip() and ':' in l])} - {speaker}")
    else:
        # 空行はそのまま保持
        english_lines.append("")
        japanese_lines.append("")

# 結果を保存
with open("fr-onde-en.txt", "w", encoding="utf-8") as f:
    for line in english_lines:
        f.write(line + "\n")

with open("fr-onde-ja.txt", "w", encoding="utf-8") as f:
    for line in japanese_lines:
        f.write(line + "\n")

if args.test:
    print(f"[TEST] 処理完了: {len([l for l in lines if l.strip() and ':' in l])}行をテスト処理")
    print("[TEST] 実際のファイルは生成されませんでした")
else:
    print(f"翻訳完了: 英語版 fr-onde-en.txt、日本語版 fr-onde-ja.txt を生成")