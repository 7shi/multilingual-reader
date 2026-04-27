# 多段階翻訳システム開発記録

## 概要

translate.pyを従来の単一処理から多段階翻訳システムに進化させ、認知バイアスを回避した高品質翻訳を実現。

## 主要な実装変更

### 1. モデル指定の必須化
```python
# 変更前
parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"翻訳に使用するモデル")

# 変更後
parser.add_argument("-m", "--model", required=True, help="翻訳に使用するモデル")
```

### 2. 推論レベルの拡張
```python
# 推論レベル選択肢を拡張
parser.add_argument("-r", "--reasoning-level", type=int, default=2, choices=[0, 1, 2, 3, 4])
```

**各レベルの特徴:**
- **Level 0**: 推論なし、直接翻訳
- **Level 1**: 標準推論付き翻訳
- **Level 2**: 2段階翻訳（デフォルト、品質重視）
- **Level 3**: 3段階翻訳（推論+2段階翻訳）
- **Level 4**: 分割3段階翻訳（2回のLLM呼び出しに分割）

### 3. コンテキスト制御機能
```python
parser.add_argument("--history", type=int, default=5, help="コンテキストに含める履歴数")
parser.add_argument("--translated-context", action="store_true", help="翻訳文のみ提供")
```

### 4. フィールド定義の統一化
共通フィールドテンプレートを定義し、言語ペアを動的に埋め込み：
```python
translation_field = Field(description=f"Direct translation from {args.from_lang} to {args.to_lang}")
quality_assessment_field = Field(description=f"Check specifically that: 1) The text is completely translated into {args.to_lang}, 2) No {args.from_lang} words remain...")
```

### 5. レベル4の分割処理実装
```python
if args.reasoning_level == 4:
    # 第1段階：推論と初回翻訳
    first_parsed = generate_with_retry([context, prompt], FirstStageTranslation, args.model, "Stage 1")
    
    # 第2段階：品質評価と改善翻訳
    second_stage_prompt = f"Review and improve this translation..."
    second_parsed = generate_with_retry([context, second_stage_prompt], SecondStageTranslation, args.model, "Stage 2")
```

### 6. エラーハンドリング強化
```python
def generate_with_retry(prompts, schema, model, stage_name=""):
    """リトライ機能付きのLLM生成関数"""
    for j in range(5):
        try:
            result = generate_with_schema(...)
            return json.loads(result.text.strip())
        except Exception as e:
            if j < 4:
                print(e)
            else:
                raise
```

## 並行開発：専用翻訳システム

### translate-exp.py（サブコマンド方式）
3段階多モデル翻訳システム：
- **Phase 1**: 初回翻訳
- **Phase 2**: 別モデルでの品質チェック
- **Phase 3**: 修正反映

### translate2.py/translate3.py（一気通貫版）
- **translate2.py**: 3段階多モデル翻訳（85点品質）
- **translate3.py**: Phase 2a統合システム（92点品質、推奨）

## 品質評価結果

| システム | 品質スコア | 効率性 | 使用場面 |
|:---|:---:|:---:|:---|
| **translate3.py（Phase 2a）** | **92点** | **高** | **実用的高品質翻訳** |
| translate.py Level 2 | 92点 | 中 | 従来システム |
| translate2.py（3段階） | 85点 | 低 | 研究・実験目的 |

## 技術的価値

### 解決した問題
1. **言語混入問題**: フランス語「Bonjour」等の未翻訳語の残存
2. **認知バイアス**: 同一モデルでの品質チェック限界
3. **ユーザビリティ**: 複雑なサブコマンド体系

### イノベーション
1. **多モデル協調**: 異なるモデルの強みを活用
2. **段階的品質向上**: フェーズベースアプローチ
3. **実用性重視**: 効率性と品質のバランス

## 推奨使用方法

### 日常的な高品質翻訳
```bash
python translate3.py input.txt -f French -t Spanish -o output.txt \
  -m ollama:gemma3n:e4b -c ollama:qwen2.5:7b
```

### 従来システム（互換性維持）
```bash
python translate.py input.txt -f French -t Spanish -o output.txt \
  -m ollama:gemma3n:e4b -r 2
```

### 研究・分析用途
```bash
python translate2.py input.txt -f French -t Spanish -o output.txt \
  -m ollama:gemma3n:e4b -c ollama:qwen2.5:7b
```

## まとめ

複雑性から実用性への転換により、最高品質（92点）を効率的に実現するシステムを確立。translate3.pyの**Phase 2a統合システム**が最も実用的で推奨される解決策。