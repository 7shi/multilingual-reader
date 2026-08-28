#!/usr/bin/env python3
"""
Inter-evaluator comparison analysis script

Compares the evaluation results of three evaluators (Gemini-2.5-flash, gpt-oss-20b,
gpt-oss-120b), computes statistical metrics, and determines whether migration from
Gemini to gpt-oss-120b is feasible.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import numpy as np
from scipy import stats

# Paths to SCORES.txt files
SCORES_FILES = {
    'gemini-2.5-flash': '../gemini-2.5-flash/SCORES.txt',
    'gpt-oss-20b': '../gpt-oss-20b/SCORES.txt',
    'gpt-oss-120b': '../gpt-oss-120b/SCORES.txt',
    'qwen3.6': '../qwen3.6/SCORES.txt',
    'gemma-4-31b': '../gemma-4-31b/SCORES.txt',
}

OUTPUT_JSON = 'stats.json'


def parse_scores_file(filepath: str) -> Dict[str, int]:
    """
    Parse a SCORES.txt file and return a {model name: score} dictionary

    Example format:
        1→aya-expanse-32b-0: 76
        aya-expanse-32b-0: 76  (also supported without a number)
    """
    scores = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Pattern: "number→model name: score" or "model name: score"
            match = re.search(r'(?:\d+→)?(.+?):\s*(\d+)', line)
            if match:
                model_name = match.group(1).strip()
                score = int(match.group(2))
                scores[model_name] = score

    return scores


def calculate_basic_stats(scores: Dict[str, int]) -> Dict:
    """Compute basic statistics"""
    values = np.array(list(scores.values()))

    # Distribution by score range
    ranges = {
        '0-20': int(np.sum((values >= 0) & (values <= 20))),
        '21-40': int(np.sum((values >= 21) & (values <= 40))),
        '41-60': int(np.sum((values >= 41) & (values <= 60))),
        '61-80': int(np.sum((values >= 61) & (values <= 80))),
        '81-100': int(np.sum((values >= 81) & (values <= 100))),
    }

    # Distribution of high-score bands
    high_score_counts = {
        '>=95': int(np.sum(values >= 95)),
        '>=96': int(np.sum(values >= 96)),
        '>=97': int(np.sum(values >= 97)),
        '>=98': int(np.sum(values >= 98)),
        '>=99': int(np.sum(values >= 99)),
        '100': int(np.sum(values == 100)),
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
        'high_score_counts': high_score_counts,
    }


def calculate_correlations(scores1: Dict[str, int], scores2: Dict[str, int],
                          name1: str, name2: str) -> Dict:
    """Compute correlation coefficients between two evaluators"""
    # Extract common model names
    common_models = set(scores1.keys()) & set(scores2.keys())

    values1 = np.array([scores1[m] for m in sorted(common_models)])
    values2 = np.array([scores2[m] for m in sorted(common_models)])

    # Pearson correlation coefficient
    pearson_r, pearson_p = stats.pearsonr(values1, values2)

    # Spearman rank correlation coefficient
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
    """Compute agreement between two evaluators"""
    common_models = set(scores1.keys()) & set(scores2.keys())

    values1 = np.array([scores1[m] for m in sorted(common_models)])
    values2 = np.array([scores2[m] for m in sorted(common_models)])

    # Differences
    diffs = values1 - values2
    abs_diffs = np.abs(diffs)

    # Mean absolute error (MAE)
    mae = float(np.mean(abs_diffs))

    # Root mean square error (RMSE)
    rmse = float(np.sqrt(np.mean(diffs ** 2)))

    # Agreement rate within +/- N points
    within_5pts = float(np.mean(abs_diffs <= 5))
    within_10pts = float(np.mean(abs_diffs <= 10))

    # Agreement rate for top-10% models
    threshold = 90
    top_in_1 = set(m for m in common_models if scores1[m] >= threshold)
    top_in_2 = set(m for m in common_models if scores2[m] >= threshold)
    if len(top_in_1 | top_in_2) > 0:
        top10_agreement = len(top_in_1 & top_in_2) / len(top_in_1 | top_in_2)
    else:
        top10_agreement = 1.0  # Treat as agreement when neither has a match

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
    """Extract the family name from a model name"""
    # Family name patterns
    families = [
        'aya-expanse',
        'command-r7b', 'command-r',  # check r7b first
        'gemma3n-e4b', 'gemma3', 'gemma2',  # check more specific ones first
        'gpt-oss',
        'llama4-scout', 'llama3.3', 'llama',
        'ministral-3',
        'mistral-small3.2', 'mistral',  # check small3.2 first
        'mixtral',
        'phi4',
        'qwen3',
    ]

    for family in families:
        if model_name.startswith(family):
            return family

    return 'unknown'


def analyze_systematic_bias(all_scores: Dict[str, Dict[str, int]]) -> Dict:
    """Analyze systematic bias"""
    result = {
        'by_model_family': {},
        'by_inference_level': {},
        'by_temperature': {},
    }

    # Model names common to all evaluators
    common_models = set(all_scores['gemini-2.5-flash'].keys())
    for scores in all_scores.values():
        common_models &= set(scores.keys())

    # Average difference by model family
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
        # Difference between Gemini and gpt-oss-120b
        if data['gemini-2.5-flash'] and data['gpt-oss-120b']:
            result['by_model_family'][family]['gemini_gpt120b_diff'] = \
                float(np.mean(data['gemini-2.5-flash']) - np.mean(data['gpt-oss-120b']))

    # Analysis by inference level
    level_data = {}
    for model in common_models:
        # Extract level 0-4, tr4-6, etc.
        if re.search(r'-\d$', model):  # ends with -0,-1,...,-4
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

    # Analysis by temperature setting
    temp_data = {}
    for model in common_models:
        # Extract -05, -10, -15, -20, -25
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
    """Extract problem cases"""
    gemini = all_scores['gemini-2.5-flash']
    gpt120b = all_scores['gpt-oss-120b']

    common_models = set(gemini.keys()) & set(gpt120b.keys())

    # Cases with a large discrepancy
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

    # Zero-score cases
    zero_scores = []
    for name, scores in all_scores.items():
        for model, score in scores.items():
            if score == 0:
                zero_scores.append({
                    'model': model,
                    'evaluator': name,
                })

    # Reversal cases (one evaluator scores >= 80, the other <= 50)
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
        'large_discrepancy': large_discrepancy[:30],  # TOP 30
        'zero_scores': zero_scores,
        'reversals': reversals,
    }


def make_migration_decision(correlations: Dict, agreement: Dict,
                           systematic_bias: Dict) -> Dict:
    """Make the migration decision"""
    # Retrieve gemini vs gpt-oss-120b data
    # Pair name format: "gemini25flash_vs_gptoss120b"
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

    # Decision criteria
    reasons = []

    if spearman >= 0.85:
        reasons.append(f"✅ Spearman rank correlation: {spearman:.3f} >= 0.85 (pass)")
    elif spearman >= 0.70:
        reasons.append(f"⚠️ Spearman rank correlation: {spearman:.3f} (0.70-0.85 range)")
    else:
        reasons.append(f"❌ Spearman rank correlation: {spearman:.3f} < 0.70 (fail)")

    if top10 >= 0.75:
        reasons.append(f"✅ Top-10% agreement rate: {top10:.3f} >= 0.75 (pass)")
    elif top10 >= 0.60:
        reasons.append(f"⚠️ Top-10% agreement rate: {top10:.3f} (0.60-0.75 range)")
    else:
        reasons.append(f"❌ Top-10% agreement rate: {top10:.3f} < 0.60 (fail)")

    if within_10 >= 0.70:
        reasons.append(f"✅ Agreement rate within +/-10 points: {within_10:.3f} >= 0.70 (pass)")
    elif within_10 >= 0.60:
        reasons.append(f"⚠️ Agreement rate within +/-10 points: {within_10:.3f} (0.60-0.70 range)")
    else:
        reasons.append(f"❌ Agreement rate within +/-10 points: {within_10:.3f} < 0.60 (fail)")

    # Whether the systematic bias can be corrected
    max_family_bias = max(
        abs(data.get('gemini_gpt120b_diff', 0))
        for data in systematic_bias['by_model_family'].values()
    )

    if max_family_bias <= 15:
        reasons.append(f"✅ Max per-model-family bias: {max_family_bias:.1f} points (correctable)")
    else:
        reasons.append(f"⚠️ Max per-model-family bias: {max_family_bias:.1f} points (correction needed)")

    # Overall decision
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
    """Main process"""
    print("=" * 60)
    print("Inter-evaluator comparison analysis")
    print("=" * 60)

    # 1. Load data
    print("\n[1] Loading SCORES.txt files...")
    all_scores = {}
    for name, filepath in SCORES_FILES.items():
        full_path = Path(__file__).parent / filepath
        if not full_path.exists():
            print(f"Warning: {full_path} not found. Skipping.")
            continue

        all_scores[name] = parse_scores_file(str(full_path))
        print(f"  - {name}: {len(all_scores[name])} items")

    # Check that the item counts match
    counts = [len(scores) for scores in all_scores.values()]
    if len(set(counts)) > 1:
        print(f"Warning: item counts do not match: {counts}")
    else:
        print(f"  ✓ Confirmed {counts[0]} items for all evaluators")

    # 2. Compute basic statistics
    print("\n[2] Computing basic statistics...")
    basic_stats = {}
    for name, scores in all_scores.items():
        basic_stats[name] = calculate_basic_stats(scores)
        stats_data = basic_stats[name]
        print(f"\n  {name}:")
        print(f"    Mean: {stats_data['mean']:.2f}, Median: {stats_data['median']:.2f}")
        print(f"    Std dev: {stats_data['std']:.2f}, Range: [{stats_data['min']}, {stats_data['max']}]")

    # 3. Correlation analysis
    print("\n[3] Computing correlation coefficients...")
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
            print(f"    Pearson: {corr['pearson']:.3f} (p={corr['pearson_p']:.3e})")
            print(f"    Spearman: {corr['spearman']:.3f} (p={corr['spearman_p']:.3e})")

    # 4. Agreement analysis
    print("\n[4] Computing agreement...")
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
            print(f"    MAE: {agree['mae']:.2f} pts, RMSE: {agree['rmse']:.2f} pts")
            print(f"    Within +/-5 pts: {agree['within_5pts']:.1%}, Within +/-10 pts: {agree['within_10pts']:.1%}")
            print(f"    Top-10% agreement rate: {agree['top10_agreement']:.1%}")

    # 5. Systematic bias detection
    print("\n[5] Analyzing systematic bias...")
    systematic_bias = analyze_systematic_bias(all_scores)
    print(f"  - Model families: {len(systematic_bias['by_model_family'])} types")
    print(f"  - Inference levels: {len(systematic_bias['by_inference_level'])} types")
    print(f"  - Temperature settings: {len(systematic_bias['by_temperature'])} types")

    # 6. Extract problem cases
    print("\n[6] Extracting problem cases...")
    problem_cases = find_problem_cases(all_scores)
    print(f"  - Large discrepancies (>=30 pts): {len(problem_cases['large_discrepancy'])} cases")
    print(f"  - Zero-score evaluations: {len(problem_cases['zero_scores'])} cases")
    print(f"  - Reversal cases: {len(problem_cases['reversals'])} cases")

    # 7. Migration decision
    print("\n[7] Making migration decision...")
    migration_decision = make_migration_decision(correlations, agreement, systematic_bias)

    judgment_labels = {
        'possible': '✅ Migration possible',
        'conditional': '⚠️ Conditional migration possible',
        'impossible': '❌ Migration not recommended',
    }

    print(f"\n  Decision: {judgment_labels[migration_decision['judgment']]}")
    print("\n  Reasons:")
    for reason in migration_decision['reasons']:
        print(f"    {reason}")

    # 8. JSON output
    print(f"\n[8] Saving results to {OUTPUT_JSON}...")
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

    print(f"  ✓ Saved: {output_path}")
    print("\n" + "=" * 60)
    print("Analysis complete")
    print("=" * 60)


if __name__ == '__main__':
    main()
