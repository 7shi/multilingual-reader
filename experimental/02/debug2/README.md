# debug2: KV キャッシュ調査

## 目的

`translate.py` の KV キャッシュが実際に効いているかを `prompt_eval_duration`（prefill 時間）で計測し、問題箇所を特定して修正した。

---

## 調査方法

`call_llm` の戻り値 `response.chunks[-1]` から `prompt_eval_count` / `prompt_eval_duration` を取得し、prefill 速度をログに出力するよう `translate.py` を拡張した。

```
prefill: 844 tokens, 0.42s, 1986 tps
```

KV キャッシュが効いているかどうかは **duration** で判定できる。キャッシュが有効なら増分トークンだけ計算されるため 0.5s 以内に完了する。キャッシュミスの場合は全トークンを再計算するためトークン数に比例して長くなる（800〜1400 tokens で 3〜5s）。

なお表示している tps はキャッシュ済みトークンを含む総トークン数から算出しているため、キャッシュヒット時は実際の計算量より大きく見える。差分トークン数で計算すると概ね 250 tps 前後（ハードウェアの実際の prefill 速度）になる。

---

## 発見した問題

修正前の `call_llm` では、`chat_history` からロール情報を除いてコンテンツ文字列だけを取り出していた：

```python
contents = [msg["content"] for msg in chat_history[1:]]
generate_with_schema(contents, system_prompt=system_content, ...)
```

`generate_with_schema`（旧版）は `contents: List[str]` を全て `role: user` として Ollama に送信していた。これにより：

- 翻訳応答（本来 `role: assistant`）が次リクエストで `role: user` として再送信される
- Ollama のトークン列が変わり KV キャッシュが無効化される
- サマリー生成後の翻訳が毎回全再評価（3〜5s）になっていた

### 修正前のログ（サマリー後に失速）

```
[Generating summary after translation 10]
prefill: 1035 tokens, 0.68s   ← サマリー生成
prefill: 1129 tokens, 4.31s   ← i=11: 全再評価（KV キャッシュ無効）
prefill: 1181 tokens, 4.43s   ← i=12: 回復せず
...以降ずっと 4〜5s
```

---

## 修正

`llm7shi` を v0.10.1 にアップデートし、`generate_with_schema` が `List[Dict[str, str]]`（OpenAI format）を受け取れるようになったことを確認。`chat_history` をそのまま渡すよう変更：

```python
# 変更後
generate_with_schema(chat_history, ...)
```

`system` / `user` / `assistant` のロールがそのまま Ollama に渡り、前リクエストの応答トークン列と一致するため KV キャッシュが有効になった。

### 修正後のログ

```
[Generating summary after translation 10]
prefill: 1035 tokens, 0.68s   ← サマリー生成
prefill: 1227 tokens, 0.22s   ← i=11: KV キャッシュ有効（0.2s 台）
prefill: 1287 tokens, 0.32s   ← i=12: 継続して高速
...
[Compressing history after translation 15]
prefill:  786 tokens, 3.00s   ← 圧縮直後のみ cold start（prefix 変化のため不可避）
prefill:  883 tokens, 0.31s   ← 次の翻訳からは高速
```

---

## `--no-summary-history` オプションについて

調査中に「サマリーを `chat_history` に追加しない」`--no-summary-history` オプションも実装・比較した。

このオプションではサマリー削除後にコンテキストが縮小するため、Ollama がプレフィックス一致できずサマリー直後に毎回全再評価（3〜5s）が発生する。修正後の通常 glossary モードではサマリー直後も 0.2s なので、このオプションは不要と結論した。

---

## 評価結果（gemma3:27b）

| バリアント | 評価（3回中央値） |
|---|---|
| `glossary` | 95点 |
| `glossary-no-hist` | 96点 |

品質に差はなく、KV キャッシュ効率では `glossary` が優位。

---

## 残る cold start

圧縮（スライド）直後の翻訳は prefix が変わるため常に cold start（約 3.5s）になる。これはアーキテクチャ上の固定コストで回避不可。
