#!/usr/bin/env python3
"""
評価者間比較分析スクリプト

3つの評価者(Gemini-2.5-flash, gpt-oss-20b, gpt-oss-120b)の評価結果を比較し、
統計的指標を計算してGeminiからgpt-oss-120bへの移行可否を判定する。
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import numpy as np
from scipy import stats

# SCORES.txtファイルのパス設定
SCORES_FILES = {
    'gemini-2.5-flash': '../gemini-2.5-flash/SCORES.txt',
    'gpt-oss-20b': '../gpt-oss-20b/SCORES.txt',
    'gpt-oss-120b': '../gpt-oss-120b/SCORES.txt',
}

OUTPUT_JSON = 'stats.json'


def parse_scores_file(filepath: str) -> Dict[str, int]:
    """
    SCORES.txtファイルをパースして{モデル名: スコア}の辞書を返す

    フォーマット例:
        1→aya-expanse-32b-0: 76/100点
        aya-expanse-32b-0: 76/100点  (番号なしも対応)
    """
    scores = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # パターン: "番号→モデル名: スコア/100点" または "モデル名: スコア/100点"
            match = re.search(r'(?:\d+→)?(.+?):\s*(\d+)/100点', line)
            if match:
                model_name = match.group(1).strip()
                score = int(match.group(2))
                scores[model_name] = score

    return scores


def calculate_basic_stats(scores: Dict[str, int]) -> Dict:
    """基本統計量を計算"""
    values = np.array(list(scores.values()))

    # スコアレンジ別の分布
    ranges = {
        '0-20': int(np.sum((values >= 0) & (values <= 20))),
        '21-40': int(np.sum((values >= 21) & (values <= 40))),
        '41-60': int(np.sum((values >= 41) & (values <= 60))),
        '61-80': int(np.sum((values >= 61) & (values <= 80))),
        '81-100': int(np.sum((values >= 81) & (values <= 100))),
    }

    return {
        'mean': float(np.mean(values)),
        'median': float(np.median(values)),
        'std': float(np.std(values, ddof=1)),
        'min': int(np.min(values)),
        'max': int(np.max(values)),
        'q25': float(np.percentile(values, 25)),
        'q75': float(np.percentile(values, 75)),
        'count': len(values),
        'score_ranges': ranges,
    }


def calculate_correlations(scores1: Dict[str, int], scores2: Dict[str, int],
                          name1: str, name2: str) -> Dict:
    """2つの評価者間の相関係数を計算"""
    # 共通のモデル名を抽出
    common_models = set(scores1.keys()) & set(scores2.keys())

    values1 = np.array([scores1[m] for m in sorted(common_models)])
    values2 = np.array([scores2[m] for m in sorted(common_models)])

    # ピアソン相関係数
    pearson_r, pearson_p = stats.pearsonr(values1, values2)

    # スピアマン順位相関係数
    spearman_r, spearman_p = stats.spearmanr(values1, values2)

    return {
        'pair': f'{name1}_vs_{name2}',
        'num_common': len(common_models),
        'pearson': float(pearson_r),
        'pearson_p': float(pearson_p),
        'spearman': float(spearman_r),
        'spearman_p': float(spearman_p),
    }


def calculate_agreement(scores1: Dict[str, int], scores2: Dict[str, int],
                       name1: str, name2: str) -> Dict:
    """2つの評価者間の一致度を計算"""
    common_models = set(scores1.keys()) & set(scores2.keys())

    values1 = np.array([scores1[m] for m in sorted(common_models)])
    values2 = np.array([scores2[m] for m in sorted(common_models)])

    # 差分
    diffs = values1 - values2
    abs_diffs = np.abs(diffs)

    # 平均絶対誤差(MAE)
    mae = float(np.mean(abs_diffs))

    # 二乗平均平方根誤差(RMSE)
    rmse = float(np.sqrt(np.mean(diffs ** 2)))

    # ±N点範囲内の一致率
    within_5pts = float(np.mean(abs_diffs <= 5))
    within_10pts = float(np.mean(abs_diffs <= 10))

    # 上位10%モデルの一致率
    threshold = 90
    top_in_1 = set(m for m in common_models if scores1[m] >= threshold)
    top_in_2 = set(m for m in common_models if scores2[m] >= threshold)
    if len(top_in_1 | top_in_2) > 0:
        top10_agreement = len(top_in_1 & top_in_2) / len(top_in_1 | top_in_2)
    else:
        top10_agreement = 1.0  # 両方とも該当なしの場合は一致とみなす

    return {
        'pair': f'{name1}_vs_{name2}',
        'mae': mae,
        'rmse': rmse,
        'within_5pts': within_5pts,
        'within_10pts': within_10pts,
        'top10_agreement': float(top10_agreement),
        'mean_diff': float(np.mean(diffs)),
        'std_diff': float(np.std(diffs, ddof=1)),
    }


def extract_model_family(model_name: str) -> str:
    """モデル名からファミリー名を抽出"""
    # ファミリー名のパターン
    families = [
        'aya-expanse',
        'command-r7b', 'command-r',  # r7bを先にチェック
        'gemma3n-e4b', 'gemma3', 'gemma2',  # より具体的なものを先に
        'gpt-oss',
        'llama4-scout', 'llama3.3', 'llama',
        'ministral-3',
        'mistral-small3.2', 'mistral',  # small3.2を先にチェック
        'mixtral',
        'phi4',
        'qwen3',
    ]

    for family in families:
        if model_name.startswith(family):
            return family

    return 'unknown'


def analyze_systematic_bias(all_scores: Dict[str, Dict[str, int]]) -> Dict:
    """系統的バイアスを分析"""
    result = {
        'by_model_family': {},
        'by_inference_level': {},
        'by_temperature': {},
    }

    # すべての評価者で共通のモデル名
    common_models = set(all_scores['gemini-2.5-flash'].keys())
    for scores in all_scores.values():
        common_models &= set(scores.keys())

    # モデルファミリー別の平均差
    family_data = {}
    for model in common_models:
        family = extract_model_family(model)
        if family not in family_data:
            family_data[family] = {name: [] for name in all_scores.keys()}

        for name, scores in all_scores.items():
            family_data[family][name].append(scores[model])

    for family, data in family_data.items():
        result['by_model_family'][family] = {
            name: float(np.mean(values))
            for name, values in data.items()
        }
        # Geminiとgpt-oss-120bの差
        if data['gemini-2.5-flash'] and data['gpt-oss-120b']:
            result['by_model_family'][family]['gemini_gpt120b_diff'] = \
                float(np.mean(data['gemini-2.5-flash']) - np.mean(data['gpt-oss-120b']))

    # 推論レベル別の分析
    level_data = {}
    for model in common_models:
        # レベル0-4, tr4-6などを抽出
        if re.search(r'-\d$', model):  # 末尾が-0,-1,...,-4
            level = model[-1]
        elif 'tr4' in model:
            level = 'tr4'
        elif 'tr5' in model:
            level = 'tr5'
        elif 'tr6' in model:
            level = 'tr6'
        else:
            continue

        if level not in level_data:
            level_data[level] = {name: [] for name in all_scores.keys()}

        for name, scores in all_scores.items():
            level_data[level][name].append(scores[model])

    for level, data in level_data.items():
        result['by_inference_level'][level] = {
            name: float(np.mean(values))
            for name, values in data.items()
        }

    # 温度設定別の分析
    temp_data = {}
    for model in common_models:
        # -05, -10, -15, -20, -25を抽出
        temp_match = re.search(r'-(\d{2})(?:-[ab])?$', model)
        if temp_match:
            temp = temp_match.group(1)
            if temp not in temp_data:
                temp_data[temp] = {name: [] for name in all_scores.keys()}

            for name, scores in all_scores.items():
                temp_data[temp][name].append(scores[model])

    for temp, data in temp_data.items():
        result['by_temperature'][temp] = {
            name: float(np.mean(values))
            for name, values in data.items()
        }

    return result


def find_problem_cases(all_scores: Dict[str, Dict[str, int]]) -> Dict:
    """問題ケースを抽出"""
    gemini = all_scores['gemini-2.5-flash']
    gpt120b = all_scores['gpt-oss-120b']

    common_models = set(gemini.keys()) & set(gpt120b.keys())

    # 乖離が大きいケース
    large_discrepancy = []
    for model in common_models:
        diff = abs(gemini[model] - gpt120b[model])
        if diff >= 30:
            large_discrepancy.append({
                'model': model,
                'gemini_score': gemini[model],
                'gpt120b_score': gpt120b[model],
                'diff': int(diff),
            })

    large_discrepancy.sort(key=lambda x: x['diff'], reverse=True)

    # 0点評価ケース
    zero_scores = []
    for name, scores in all_scores.items():
        for model, score in scores.items():
            if score == 0:
                zero_scores.append({
                    'model': model,
                    'evaluator': name,
                })

    # 逆転ケース(一方が80点以上、もう一方が50点以下)
    reversals = []
    for model in common_models:
        g_score = gemini[model]
        gpt_score = gpt120b[model]

        if (g_score >= 80 and gpt_score <= 50) or (g_score <= 50 and gpt_score >= 80):
            reversals.append({
                'model': model,
                'gemini_score': g_score,
                'gpt120b_score': gpt_score,
                'diff': int(g_score - gpt_score),
            })

    return {
        'large_discrepancy': large_discrepancy[:30],  # TOP30
        'zero_scores': zero_scores,
        'reversals': reversals,
    }


def make_migration_decision(correlations: Dict, agreement: Dict,
                           systematic_bias: Dict) -> Dict:
    """移行判定を行う"""
    # gemini vs gpt-oss-120bのデータを取得
    # ペア名の形式: "gemini25flash_vs_gptoss120b"
    gemini_gpt120b_corr = next(
        c for c in correlations.values()
        if 'gemini25flash' in c['pair'].lower() and 'gptoss120b' in c['pair'].lower()
    )
    gemini_gpt120b_agree = next(
        a for a in agreement.values()
        if 'gemini25flash' in a['pair'].lower() and 'gptoss120b' in a['pair'].lower()
    )

    spearman = gemini_gpt120b_corr['spearman']
    top10 = gemini_gpt120b_agree['top10_agreement']
    within_10 = gemini_gpt120b_agree['within_10pts']

    # 判定基準
    reasons = []

    if spearman >= 0.85:
        reasons.append(f"✅ スピアマン順位相関係数: {spearman:.3f} ≥ 0.85 (合格)")
    elif spearman >= 0.70:
        reasons.append(f"⚠️ スピアマン順位相関係数: {spearman:.3f} (0.70-0.85の範囲)")
    else:
        reasons.append(f"❌ スピアマン順位相関係数: {spearman:.3f} < 0.70 (不合格)")

    if top10 >= 0.75:
        reasons.append(f"✅ 上位10%一致率: {top10:.3f} ≥ 0.75 (合格)")
    elif top10 >= 0.60:
        reasons.append(f"⚠️ 上位10%一致率: {top10:.3f} (0.60-0.75の範囲)")
    else:
        reasons.append(f"❌ 上位10%一致率: {top10:.3f} < 0.60 (不合格)")

    if within_10 >= 0.70:
        reasons.append(f"✅ ±10点範囲内一致率: {within_10:.3f} ≥ 0.70 (合格)")
    elif within_10 >= 0.60:
        reasons.append(f"⚠️ ±10点範囲内一致率: {within_10:.3f} (0.60-0.70の範囲)")
    else:
        reasons.append(f"❌ ±10点範囲内一致率: {within_10:.3f} < 0.60 (不合格)")

    # 系統的バイアスの補正可能性
    max_family_bias = max(
        abs(data.get('gemini_gpt120b_diff', 0))
        for data in systematic_bias['by_model_family'].values()
    )

    if max_family_bias <= 15:
        reasons.append(f"✅ 最大モデルファミリー別バイアス: {max_family_bias:.1f}点 (補正可能)")
    else:
        reasons.append(f"⚠️ 最大モデルファミリー別バイアス: {max_family_bias:.1f}点 (補正が必要)")

    # 総合判定
    if spearman >= 0.85 and top10 >= 0.75 and within_10 >= 0.70:
        judgment = "possible"
    elif spearman < 0.70 or top10 < 0.60 or within_10 < 0.60:
        judgment = "impossible"
    else:
        judgment = "conditional"

    return {
        'judgment': judgment,
        'spearman_correlation': float(spearman),
        'top10_agreement': float(top10),
        'within_10pts_rate': float(within_10),
        'max_family_bias': float(max_family_bias),
        'reasons': reasons,
    }


def main():
    """メイン処理"""
    print("=" * 60)
    print("評価者間比較分析")
    print("=" * 60)

    # 1. データ読み込み
    print("\n[1] SCORES.txtファイルを読み込み中...")
    all_scores = {}
    for name, filepath in SCORES_FILES.items():
        full_path = Path(__file__).parent / filepath
        if not full_path.exists():
            print(f"エラー: {full_path} が見つかりません")
            return

        all_scores[name] = parse_scores_file(str(full_path))
        print(f"  - {name}: {len(all_scores[name])} 項目")

    # 項目数の一致確認
    counts = [len(scores) for scores in all_scores.values()]
    if len(set(counts)) > 1:
        print(f"警告: 項目数が一致しません: {counts}")
    else:
        print(f"  ✓ 全評価者で {counts[0]} 項目を確認")

    # 2. 基本統計計算
    print("\n[2] 基本統計量を計算中...")
    basic_stats = {}
    for name, scores in all_scores.items():
        basic_stats[name] = calculate_basic_stats(scores)
        stats_data = basic_stats[name]
        print(f"\n  {name}:")
        print(f"    平均: {stats_data['mean']:.2f}, 中央値: {stats_data['median']:.2f}")
        print(f"    標準偏差: {stats_data['std']:.2f}, 範囲: [{stats_data['min']}, {stats_data['max']}]")

    # 3. 相関分析
    print("\n[3] 相関係数を計算中...")
    correlations = {}
    evaluators = list(all_scores.keys())
    for i in range(len(evaluators)):
        for j in range(i + 1, len(evaluators)):
            name1, name2 = evaluators[i], evaluators[j]
            corr = calculate_correlations(
                all_scores[name1], all_scores[name2],
                name1.replace('.', '').replace('-', ''),
                name2.replace('.', '').replace('-', '')
            )
            correlations[corr['pair']] = corr
            print(f"\n  {name1} vs {name2}:")
            print(f"    ピアソン: {corr['pearson']:.3f} (p={corr['pearson_p']:.3e})")
            print(f"    スピアマン: {corr['spearman']:.3f} (p={corr['spearman_p']:.3e})")

    # 4. 一致度分析
    print("\n[4] 一致度を計算中...")
    agreement = {}
    for i in range(len(evaluators)):
        for j in range(i + 1, len(evaluators)):
            name1, name2 = evaluators[i], evaluators[j]
            agree = calculate_agreement(
                all_scores[name1], all_scores[name2],
                name1.replace('.', '').replace('-', ''),
                name2.replace('.', '').replace('-', '')
            )
            agreement[agree['pair']] = agree
            print(f"\n  {name1} vs {name2}:")
            print(f"    MAE: {agree['mae']:.2f}点, RMSE: {agree['rmse']:.2f}点")
            print(f"    ±5点以内: {agree['within_5pts']:.1%}, ±10点以内: {agree['within_10pts']:.1%}")
            print(f"    上位10%一致率: {agree['top10_agreement']:.1%}")

    # 5. 系統的バイアス検出
    print("\n[5] 系統的バイアスを分析中...")
    systematic_bias = analyze_systematic_bias(all_scores)
    print(f"  - モデルファミリー: {len(systematic_bias['by_model_family'])} 種類")
    print(f"  - 推論レベル: {len(systematic_bias['by_inference_level'])} 種類")
    print(f"  - 温度設定: {len(systematic_bias['by_temperature'])} 種類")

    # 6. 問題ケース抽出
    print("\n[6] 問題ケースを抽出中...")
    problem_cases = find_problem_cases(all_scores)
    print(f"  - 大きな乖離(≥30点): {len(problem_cases['large_discrepancy'])} 件")
    print(f"  - 0点評価: {len(problem_cases['zero_scores'])} 件")
    print(f"  - 逆転ケース: {len(problem_cases['reversals'])} 件")

    # 7. 移行判定
    print("\n[7] 移行判定を実施中...")
    migration_decision = make_migration_decision(correlations, agreement, systematic_bias)

    judgment_labels = {
        'possible': '✅ 移行可能',
        'conditional': '⚠️ 条件付き移行可能',
        'impossible': '❌ 移行不可',
    }

    print(f"\n  判定結果: {judgment_labels[migration_decision['judgment']]}")
    print("\n  判定理由:")
    for reason in migration_decision['reasons']:
        print(f"    {reason}")

    # 8. JSON出力
    print(f"\n[8] 結果を {OUTPUT_JSON} に保存中...")
    output_data = {
        'metadata': {
            'num_entries': counts[0] if counts else 0,
            'evaluators': list(all_scores.keys()),
            'generated_at': datetime.now().isoformat(),
        },
        'basic_stats': basic_stats,
        'correlations': correlations,
        'agreement': agreement,
        'systematic_bias': systematic_bias,
        'problem_cases': problem_cases,
        'migration_decision': migration_decision,
    }

    output_path = Path(__file__).parent / OUTPUT_JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"  ✓ 保存完了: {output_path}")
    print("\n" + "=" * 60)
    print("分析完了")
    print("=" * 60)


if __name__ == '__main__':
    main()
