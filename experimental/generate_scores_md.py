#!/usr/bin/env python3
"""SCORES.txtからSCORES.mdを生成するスクリプト

仕様のポイント:
1. 完全にデータドリブン
   - モデル名、テスト設定、すべてSCORES.txtから自動抽出
   - ハードコーディングなし（データの存在チェックのみで判断）

2. テーブル生成
   - 推論レベル別（-r 0-4）: -r 0-4のデータがあるモデルのみ表示
   - レベル0/1/2: 各レベルのデータがあるモデルと設定を動的に抽出
   - 翻訳改善効果の検証: 0-xxと2-xxのデータを比較
   - 構造化出力の影響調査: 0-xx/1-xx と tr4/tr6 を比較
   - 自由記述式推論比較: tr5とtr6を比較

3. フラグ処理（(t), (nt)など）
   - テーブル: フラグ付きモデルとして別行で表示
   - 実用設定一覧: フラグ付きで表示するが、ソート時はベースモデル名で判断

4. モデル別実用設定一覧（各モデルの上位5項目かつ85点以上）
   - ソート順: ベースモデル名の最高スコア降順（フラグは捨象）
   - 表示: フラグ付きモデル名で表示
   - 各モデル内: スコアの降順で上位5項目のみ表示
   - 同じモデル・同じスコア: 設定をカンマ区切りで結合

5. 最大値の太字表示
   - 各テーブルの行ごとに最大スコアを太字で表示
"""

import re
from collections import defaultdict
from pathlib import Path

def parse_test_name(test_name):
    """テスト名を解析してモデル名とテスト種別を抽出"""
    # パターン例:
    # gemma2-9b-0 -> model: gemma2-9b, type: -r, variant: 0
    # gemma2-9b-0-05 -> model: gemma2-9b, type: 0-, history: 05
    # gemma2-9b-1-05 -> model: gemma2-9b, type: 1-, history: 05
    # gemma2-9b-tr4-05 -> model: gemma2-9b, type: tr4-, history: 05
    # qwen3-4b-0-t-05 -> model: qwen3-4b, type: 0-, history: 05, flag: t
    # qwen3-30b-tr4-nt-05 -> model: qwen3-30b, type: tr4-, history: 05, flag: nt
    # llama4-scout-0 -> model: llama4-scout, type: -r, variant: 0

    parts = test_name.split('-')

    # 末尾から既知のサフィックスパターンを探す
    # サフィックスの開始位置を特定
    suffix_start = len(parts)

    # 最後の部分から逆順にチェック
    i = len(parts) - 1
    while i >= 0:
        part = parts[i]

        # 数値パターン (05, 10, 15, 20, 25, 0-4など)
        if part in ['05', '10', '15', '20', '25', '0', '1', '2', '3', '4']:
            suffix_start = i
            i -= 1
            continue

        # a/b サフィックス
        if part in ['a', 'b'] and i > 0:
            suffix_start = i
            i -= 1
            continue

        # フラグ (t, nt)
        if part in ['t', 'nt'] and i > 0:
            suffix_start = i
            i -= 1
            continue

        # tr4/tr5/tr6
        if part in ['tr4', 'tr5', 'tr6'] and i > 0:
            suffix_start = i
            i -= 1
            continue

        # それ以外はモデル名の一部
        break

    # モデル名を抽出
    if suffix_start == 0:
        return None

    model_name = '-'.join(parts[:suffix_start])
    remaining = parts[suffix_start:]

    if not model_name or not remaining:
        return None

    # 残りの部分を解析
    test_type = None
    history = None
    flags = []

    i = 0
    while i < len(remaining):
        part = remaining[i]

        # -r 0-4 パターン
        if part in ['0', '1', '2', '3', '4'] and i == 0:
            test_type = '-r'
            variant = part
            i += 1
            # 次がhistoryかチェック
            if i < len(remaining) and remaining[i] in ['05', '10', '15', '20', '25']:
                history = remaining[i]
                test_type = f"{variant}-"
                i += 1
                # 次がa/bかチェック
                if i < len(remaining) and remaining[i] in ['a', 'b']:
                    history += f"-{remaining[i]}"
                    i += 1
            else:
                history = variant
        # tr4/tr5/tr6 パターン
        elif part in ['tr4', 'tr5', 'tr6']:
            test_type = f"{part}-"
            i += 1
            # ntフラグチェック
            if i < len(remaining) and remaining[i] == 'nt':
                flags.append('nt')
                i += 1
            # history
            if i < len(remaining) and remaining[i] in ['05', '10', '15', '20', '25']:
                history = remaining[i]
                i += 1
        # tフラグ（0-t-05パターン）
        elif part == 't':
            flags.append('t')
            i += 1
        else:
            i += 1

    return {
        'model': model_name,
        'type': test_type,
        'history': history,
        'flags': flags
    }

def parse_scores(scores_file):
    """SCORES.txtを解析"""
    all_scores = {}

    with open(scores_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            match = re.match(r'^(.+?):\s*(\d+)/100点$', line)
            if match:
                test_name = match.group(1)
                score = int(match.group(2))
                all_scores[test_name] = score

    return all_scores

def extract_models_from_scores(all_scores):
    """スコアデータからモデル名のリストを抽出"""
    models_set = set()

    for test_name in all_scores.keys():
        parsed = parse_test_name(test_name)
        if parsed and parsed['model']:
            models_set.add(parsed['model'])

    return sorted(models_set)

def get_test_configs_by_pattern(all_scores, pattern_type):
    """特定のパターンのテスト設定を抽出"""
    configs_set = set()

    for test_name in all_scores.keys():
        parsed = parse_test_name(test_name)
        if not parsed:
            continue

        # パターンタイプに応じて設定を抽出
        if pattern_type == '-r':
            # -r 0-4 パターン
            if parsed['type'] == '-r' and parsed['history'] in ['0', '1', '2', '3', '4']:
                configs_set.add(parsed['history'])
        elif pattern_type.startswith('level-'):
            # レベル別パターン (0-05, 1-10など)
            level = pattern_type.split('-')[1]
            if parsed['type'] == f"{level}-" and parsed['history']:
                configs_set.add(parsed['history'])
        elif pattern_type.startswith('tr'):
            # tr4, tr5, tr6パターン
            tr_num = pattern_type[2:]
            if parsed['type'] == f"tr{tr_num}-" and parsed['history']:
                configs_set.add(parsed['history'])

    return sorted(configs_set)

def has_flag_variant(all_scores, model_name, flag, pattern_prefix=''):
    """特定のモデルとフラグの組み合わせがデータに存在するかチェック"""
    for test_name in all_scores.keys():
        if not test_name.startswith(f"{model_name}-"):
            continue
        if pattern_prefix and not pattern_prefix in test_name:
            continue
        parsed = parse_test_name(test_name)
        if parsed and flag in parsed.get('flags', []):
            return True
    return False

def get_model_display_name(model_name, flags):
    """モデル表示名を生成（フラグ付き）"""
    if flags:
        return f"{model_name} ({''.join(flags)})"
    return model_name

def generate_table(f, title, models, test_configs, all_scores, column_headers=None):
    """テーブルを生成

    Args:
        f: 出力ファイル
        title: テーブルタイトル
        models: モデル情報のリスト
        test_configs: テスト設定のリスト（patternで使用）
        all_scores: スコア辞書
        column_headers: 列ヘッダー（省略時はtest_configsを使用）
    """
    if title:
        f.write(f"### {title}\n\n")

    # column_headersが指定されていない場合はtest_configsを使用
    if column_headers is None:
        column_headers = test_configs

    # ヘッダー
    f.write("| モデル |")
    for header in column_headers:
        f.write(f" {header} |")
    f.write("\n")

    f.write("|:---|")
    for _ in column_headers:
        f.write(":---:|")
    f.write("\n")

    # データ行
    for model_info in models:
        model_name = model_info['model']
        flags = model_info.get('flags', [])
        display_name = get_model_display_name(model_name, flags)

        f.write(f"| **{display_name}** |")

        max_score = -1
        scores_in_row = []

        # まず全スコアを収集して最大値を見つける
        for config in test_configs:
            test_name = model_info['pattern'].format(config=config)
            score = all_scores.get(test_name)
            scores_in_row.append(score)
            if score is not None and score > max_score:
                max_score = score

        # スコアを出力（最大値を太字に）
        for score in scores_in_row:
            if score is None:
                f.write(" - |")
            elif score == max_score and max_score >= 0:
                f.write(f" **{score}** |")
            else:
                f.write(f" {score} |")
        f.write("\n")

    f.write("\n")

def generate_markdown(all_scores, output_file):
    """SCORES.md.origと同じ形式でMarkdownを生成"""

    # モデル名とテスト設定を自動抽出
    all_models = extract_models_from_scores(all_scores)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# ローカルLLM翻訳実験\n\n")

        # 推論レベル別システム設計と実験スコア
        f.write("## 推論レベル別システム設計と実験スコア\n\n")

        # -r 0-4 のデータがあるモデルのみ抽出
        models_with_r = []
        for model in all_models:
            # -r 0-4 のいずれかのデータがあるかチェック
            has_r_data = False
            for i in range(5):
                if f"{model}-{i}" in all_scores:
                    has_r_data = True
                    break
            if has_r_data:
                models_with_r.append({'model': model, 'pattern': f'{model}-{{config}}'})

        generate_table(f, "", models_with_r, ['0', '1', '2', '3', '4'], all_scores)

        # レベル0、1、2のテーブルを動的に生成
        for level, title in [('0', 'レベル0: 直接翻訳'), ('1', 'レベル1: 推論付き翻訳'), ('2', 'レベル2: 2段階翻訳')]:
            f.write(f"### {title}\n\n")

            # このレベルのテスト設定を抽出
            configs_set = set()
            for test_name in all_scores.keys():
                parsed = parse_test_name(test_name)
                if parsed and parsed['type'] == f"{level}-" and parsed['history']:
                    # a/bサフィックスを含む履歴を処理
                    configs_set.add(parsed['history'])

            # プレフィックス付きの列ヘッダーを生成
            configs = sorted(configs_set)
            column_headers = [f"{level}-{config}" for config in configs]

            # このレベルのデータがあるモデルを抽出
            models = []
            for model in all_models:
                # 通常バージョンのデータがあるかチェック
                has_data = False
                for config in configs:
                    if f"{model}-{level}-{config}" in all_scores:
                        has_data = True
                        break
                if has_data:
                    models.append({'model': model, 'pattern': f'{model}-{level}-{{config}}'})

                # (t) バリアントのデータがあるかチェック
                has_t_data = False
                for config in configs:
                    if f"{model}-{level}-t-{config}" in all_scores:
                        has_t_data = True
                        break
                if has_t_data:
                    models.append({'model': model, 'flags': ['t'], 'pattern': f'{model}-{level}-t-{{config}}'})

            generate_table(f, "", models, configs, all_scores, column_headers)

        # 翻訳改善効果の検証（レベル0 vs レベル2）
        f.write("### 翻訳改善効果の検証（レベル0 vs レベル2）\n\n")

        # 0-xx と 2-xx の設定を収集
        configs_0 = set()
        configs_2 = set()
        for test_name in all_scores.keys():
            parsed = parse_test_name(test_name)
            if parsed and parsed['type'] == '0-' and parsed['history']:
                # 0-15, 0-25を除外、0-20は除外（0-20-a, 0-20-bのみ）
                if parsed['history'] not in ['15', '20', '25']:
                    configs_0.add(f"0-{parsed['history']}")
            elif parsed and parsed['type'] == '2-' and parsed['history']:
                # 2-15, 2-25を除外
                if parsed['history'] not in ['15', '25']:
                    configs_2.add(f"2-{parsed['history']}")

        configs = sorted(configs_0) + sorted(configs_2)

        # データがあるモデルを抽出
        models = []
        for model in all_models:
            has_data = any(f"{model}-{config}" in all_scores for config in configs)
            if has_data:
                models.append({'model': model, 'pattern': f'{model}-{{config}}'})

        generate_table(f, "", models, configs, all_scores)

        # 直接翻訳における構造化出力の影響調査（レベル0 vs tr4）
        f.write("### 直接翻訳における構造化出力の影響調査（レベル0 vs tr4）\n\n")

        # 0-xx と tr4-xx の設定を収集
        configs_0 = set()
        configs_tr4 = set()
        for test_name in all_scores.keys():
            parsed = parse_test_name(test_name)
            if parsed and parsed['type'] == '0-' and parsed['history']:
                # 0-15, 0-25を除外、0-20は除外（0-20-a, 0-20-bのみ）
                if parsed['history'] not in ['15', '20', '25']:
                    configs_0.add(f"0-{parsed['history']}")
            elif parsed and parsed['type'] == 'tr4-' and parsed['history']:
                # tr4-15, tr4-25を除外
                if parsed['history'] not in ['15', '25']:
                    configs_tr4.add(f"tr4-{parsed['history']}")

        configs = sorted(configs_0) + sorted(configs_tr4)

        # ヘッダー
        f.write("| モデル |")
        for config in configs:
            f.write(f" {config} |")
        f.write("\n")
        f.write("|:---|")
        for _ in configs:
            f.write(":---:|")
        f.write("\n")

        # データがあるモデルとバリアントを抽出
        model_configs = []
        for model in all_models:
            # 通常バージョン
            has_data = any(f"{model}-{config}" in all_scores for config in configs)
            if has_data:
                model_configs.append((model, None))

            # (nt) バリアント
            has_nt_data = False
            for config in configs:
                if config.startswith('tr4-'):
                    parts = config.split('-')
                    test_name = f"{model}-{parts[0]}-nt-{parts[1]}"
                    if test_name in all_scores:
                        has_nt_data = True
                        break
            if has_nt_data:
                model_configs.append((model, 'nt'))

        for model_base, flag_variant in model_configs:
            display_name = f"{model_base} (nt)" if flag_variant == 'nt' else model_base
            f.write(f"| **{display_name}** |")

            max_score = -1
            scores_in_row = []

            for config in configs:
                # 0-xx のデータは通常のパターン、tr4-xx はnt付きパターン
                if config.startswith('0-'):
                    if flag_variant == 'nt':
                        # ntモデルは0-xxのデータなし
                        score = None
                    else:
                        test_name = f"{model_base}-{config}"
                        score = all_scores.get(test_name)
                else:  # tr4-xx
                    if flag_variant == 'nt':
                        # tr4-05 -> tr4-nt-05
                        parts = config.split('-')
                        test_name = f"{model_base}-{parts[0]}-nt-{parts[1]}"
                    else:
                        test_name = f"{model_base}-{config}"
                    score = all_scores.get(test_name)

                scores_in_row.append(score)
                if score is not None and score > max_score:
                    max_score = score

            # スコアを出力
            for score in scores_in_row:
                if score is None:
                    f.write(" - |")
                elif score == max_score and max_score >= 0:
                    f.write(f" **{score}** |")
                else:
                    f.write(f" {score} |")
            f.write("\n")

        f.write("\n")

        # 推論付き翻訳における構造化出力の影響調査（レベル1 vs tr6）
        f.write("### 推論付き翻訳における構造化出力の影響調査（レベル1 vs tr6）\n\n")

        # 1-xx と tr6-xx の設定を収集
        configs_1 = set()
        configs_tr6 = set()
        for test_name in all_scores.keys():
            parsed = parse_test_name(test_name)
            if parsed and parsed['type'] == '1-' and parsed['history']:
                # 1-15, 1-25を除外
                if parsed['history'] not in ['15', '25']:
                    configs_1.add(f"1-{parsed['history']}")
            elif parsed and parsed['type'] == 'tr6-' and parsed['history']:
                # tr6-15, tr6-25を除外
                if parsed['history'] not in ['15', '25']:
                    configs_tr6.add(f"tr6-{parsed['history']}")

        configs = sorted(configs_1) + sorted(configs_tr6)

        # ヘッダー
        f.write("| モデル |")
        for config in configs:
            f.write(f" {config} |")
        f.write("\n")
        f.write("|:---|")
        for _ in configs:
            f.write(":---:|")
        f.write("\n")

        # データがあるモデルとバリアントを抽出
        model_configs = []
        for model in all_models:
            # 通常バージョン
            has_data = any(f"{model}-{config}" in all_scores for config in configs)
            if has_data:
                model_configs.append((model, None))

            # (nt) バリアント
            has_nt_data = False
            for config in configs:
                if config.startswith('tr6-'):
                    parts = config.split('-')
                    test_name = f"{model}-{parts[0]}-nt-{parts[1]}"
                    if test_name in all_scores:
                        has_nt_data = True
                        break
            if has_nt_data:
                model_configs.append((model, 'nt'))

        for model_base, flag_variant in model_configs:
            display_name = f"{model_base} (nt)" if flag_variant == 'nt' else model_base
            f.write(f"| **{display_name}** |")

            max_score = -1
            scores_in_row = []

            for config in configs:
                # 1-xx のデータは通常のパターン、tr6-xx はnt付きパターン
                if config.startswith('1-'):
                    if flag_variant == 'nt':
                        # ntモデルは1-xxのデータなし
                        score = None
                    else:
                        test_name = f"{model_base}-{config}"
                        score = all_scores.get(test_name)
                else:  # tr6-xx
                    if flag_variant == 'nt':
                        # tr6-05 -> tr6-nt-05
                        parts = config.split('-')
                        test_name = f"{model_base}-{parts[0]}-nt-{parts[1]}"
                    else:
                        test_name = f"{model_base}-{config}"
                    score = all_scores.get(test_name)

                scores_in_row.append(score)
                if score is not None and score > max_score:
                    max_score = score

            # スコアを出力
            for score in scores_in_row:
                if score is None:
                    f.write(" - |")
                elif score == max_score and max_score >= 0:
                    f.write(f" **{score}** |")
                else:
                    f.write(f" {score} |")
            f.write("\n")

        f.write("\n")

        # 自由記述式推論比較（tr5 vs tr6）
        f.write("### 自由記述式推論比較（tr5 vs tr6）\n\n")

        # tr5-xx と tr6-xx の設定を収集
        configs_tr5 = set()
        configs_tr6 = set()
        for test_name in all_scores.keys():
            parsed = parse_test_name(test_name)
            if parsed and parsed['type'] == 'tr5-' and parsed['history']:
                configs_tr5.add(f"tr5-{parsed['history']}")
            elif parsed and parsed['type'] == 'tr6-' and parsed['history']:
                configs_tr6.add(f"tr6-{parsed['history']}")

        configs = sorted(configs_tr5) + sorted(configs_tr6)

        # ヘッダー
        f.write("| モデル |")
        for config in configs:
            f.write(f" {config} |")
        f.write("\n")
        f.write("|:---|")
        for _ in configs:
            f.write(":---:|")
        f.write("\n")

        # データがあるモデルとバリアントを抽出
        model_configs = []
        for model in all_models:
            # 通常バージョン
            has_data = any(f"{model}-{config}" in all_scores for config in configs)
            if has_data:
                model_configs.append((model, None))

            # (nt) バリアント
            has_nt_data = False
            for config in configs:
                parts = config.split('-')
                if len(parts) == 2:
                    test_name = f"{model}-{parts[0]}-nt-{parts[1]}"
                    if test_name in all_scores:
                        has_nt_data = True
                        break
            if has_nt_data:
                model_configs.append((model, 'nt'))

        # 各モデルのデータを生成
        for model_base, flag_variant in model_configs:

                display_name = f"{model_base} (nt)" if flag_variant == 'nt' else model_base
                f.write(f"| **{display_name}** |")

                max_score = -1
                scores_in_row = []

                # tr5とtr6で異なるパターンを使用
                for config in configs:
                    # config例: 'tr5-05', 'tr6-10'
                    if flag_variant == 'nt':
                        # config内のtr5/tr6の後にnt-を挿入
                        # tr5-05 -> tr5-nt-05
                        parts = config.split('-')
                        if len(parts) == 2:  # tr5-05
                            test_name = f"{model_base}-{parts[0]}-nt-{parts[1]}"
                        else:
                            test_name = f"{model_base}-{config}"
                    else:
                        test_name = f"{model_base}-{config}"

                    score = all_scores.get(test_name)
                    scores_in_row.append(score)
                    if score is not None and score > max_score:
                        max_score = score

                # スコアを出力
                for score in scores_in_row:
                    if score is None:
                        f.write(" - |")
                    elif score == max_score and max_score >= 0:
                        f.write(f" **{score}** |")
                    else:
                        f.write(f" {score} |")
                f.write("\n")

        f.write("\n")

        # モデル別実用設定一覧
        f.write("## モデル別実用設定一覧\n\n")
        f.write("スコア変動を考慮し、各モデルの上位5項目（かつ85点以上）を実用レベルの目安として設定。\n\n")
        f.write("| モデル | スコア | 設定 |\n")
        f.write("|:---|:---:|:---|\n")

        # 85点以上のスコアを収集
        # ソート用のベースモデル名と表示用のモデル名（フラグ付き）を分けて管理
        high_scores = {}  # {(base_model, display_model, score): [configs]}
        for test_name, score in all_scores.items():
            if score >= 85:
                parsed = parse_test_name(test_name)
                if parsed:
                    # ベースモデル名（ソート用）
                    base_model = parsed['model']
                    # 表示用モデル名（フラグ付き）
                    display_model = get_model_display_name(parsed['model'], parsed['flags'])
                    config = test_name.replace(f"{parsed['model']}-", "")
                    key = (base_model, display_model, score)
                    if key not in high_scores:
                        high_scores[key] = []
                    high_scores[key].append(config)

        # ベースモデル名→(表示モデル名, スコア, 設定)でグループ化
        models_scores = {}
        for (base_model, display_model, score), configs in high_scores.items():
            if base_model not in models_scores:
                models_scores[base_model] = []
            models_scores[base_model].append((display_model, score, configs))

        # 各モデル内でスコアの降順にソートし、上位5項目のみを取得
        filtered_models_scores = {}
        for base_model, scores_list in models_scores.items():
            # スコアの降順にソート
            sorted_scores = sorted(scores_list, key=lambda x: -x[1])
            # 上位5項目のみを取得（85点以上の条件は既に満たしている）
            top_5 = sorted_scores[:5]
            if top_5:
                filtered_models_scores[base_model] = top_5

        # モデルを最高スコアの降順でソート
        sorted_models = sorted(filtered_models_scores.keys(),
                              key=lambda m: -filtered_models_scores[m][0][1])

        # 出力
        for base_model in sorted_models:
            for display_model, score, configs in filtered_models_scores[base_model]:
                # 設定をカンマ区切りで結合
                config_str = ', '.join(sorted(configs))
                f.write(f"| **{display_model}** | {score} | {config_str} |\n")

def main():
    """メイン処理"""
    scores_file = Path(__file__).parent / "SCORES.txt"
    output_file = Path(__file__).parent / "SCORES.md"

    if not scores_file.exists():
        print(f"エラー: {scores_file} が見つかりません")
        return

    print(f"SCORES.txtを読み込んでいます: {scores_file}")
    scores_by_model = parse_scores(scores_file)

    print(f"Markdownファイルを生成しています: {output_file}")
    generate_markdown(scores_by_model, output_file)

    print(f"✓ SCORES.mdを生成しました ({len(scores_by_model)}モデル)")

if __name__ == "__main__":
    main()
