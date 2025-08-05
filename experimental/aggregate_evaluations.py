# 評価結果集約スクリプト（中央値計算）

import argparse
import json
import os
import re
from statistics import median, mean, stdev
from pathlib import Path

parser = argparse.ArgumentParser(description="評価結果JSONファイルを読み込み、3回評価の中央値を計算")
parser.add_argument("files", nargs="+", help="評価結果JSONファイル（複数指定可能）")
parser.add_argument("-o", "--output", dest="output_file", help="集約結果をJSONで保存するファイル名")
parser.add_argument("--verbose", action="store_true", help="詳細な統計情報を表示")
args = parser.parse_args()

def find_evaluation_groups(files):
    """ファイルリストから評価ファイルグループを検索"""
    pattern = re.compile(r'^(.+)-([123])\.json$')
    groups = {}
    
    for filepath in files:
        filename = os.path.basename(filepath)
        match = pattern.match(filename)
        if match:
            base_name = match.group(1)
            run_number = int(match.group(2))
            
            if base_name not in groups:
                groups[base_name] = {}
            groups[base_name][run_number] = filepath
    
    # 3回すべての評価があるグループのみを返す
    complete_groups = {}
    for base_name, runs in groups.items():
        if len(runs) == 3 and all(i in runs for i in [1, 2, 3]):
            complete_groups[base_name] = runs
    
    return complete_groups

def load_evaluation_data(filepath):
    """評価JSONファイルを読み込み"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def calculate_statistics(evaluation_data_list):
    """3回の評価データから各項目の統計値を計算"""
    criteria = ['readability', 'fluency', 'terminology', 'contextual_adaptation', 'information_completeness']
    statistics = {}
    
    for criterion in criteria:
        scores = []
        for data in evaluation_data_list:
            if data and 'evaluation' in data and criterion in data['evaluation']:
                score = data['evaluation'][criterion]['score']
                scores.append(score)
        
        if len(scores) == 3:
            statistics[criterion] = {
                'median': median(scores),
                'mean': mean(scores),
                'stdev': stdev(scores) if len(scores) > 1 else 0.0,
                'scores': scores
            }
        else:
            print(f"Warning: Expected 3 scores for {criterion}, got {len(scores)}")
            statistics[criterion] = None
    
    # 総合得点を各統計値で計算
    valid_stats = [stat for stat in statistics.values() if stat is not None]
    if len(valid_stats) == 5:
        total_median = sum(stat['median'] for stat in valid_stats)
        total_mean = sum(stat['mean'] for stat in valid_stats)
        # 総合得点の標準偏差は各項目の分散の和の平方根
        total_variance = sum(stat['stdev']**2 for stat in valid_stats)
        total_stdev = total_variance**0.5
    else:
        total_median = total_mean = total_stdev = None
    
    total_scores = {
        'median': total_median,
        'mean': total_mean,
        'stdev': total_stdev
    }
    
    return statistics, total_scores

def aggregate_evaluations(files):
    """ファイルリストの評価結果を集約"""
    groups = find_evaluation_groups(files)
    results = {}
    
    for base_name, runs in groups.items():
        # 3回の評価データを読み込み
        evaluation_data_list = []
        for run_num in [1, 2, 3]:
            filepath = runs[run_num]
            data = load_evaluation_data(filepath)
            evaluation_data_list.append(data)
        
        # 統計値を計算
        statistics, total_scores = calculate_statistics(evaluation_data_list)
        
        # 最初の評価データから基本情報を取得
        first_data = evaluation_data_list[0]
        if first_data:
            results[base_name] = {
                'original_file': first_data.get('original_file'),
                'translation_file': first_data.get('translation_file'),
                'source_language': first_data.get('source_language'),
                'target_language': first_data.get('target_language'),
                'model_used': first_data.get('model_used'),
                'evaluation_files': [runs[i] for i in [1, 2, 3]],
                'statistics': statistics,
                'total_scores': total_scores
            }
    
    return results

# 集約実行
aggregated_results = aggregate_evaluations(args.files)

# 結果表示
for base_name, result in aggregated_results.items():
    total = result['total_scores']
    
    if args.verbose:
        print(f"\n{base_name}:")
        if result['statistics']:
            criteria_names = {
                'readability': '読みやすさと理解しやすさ',
                'fluency': '流暢さと自然さ          ',
                'terminology': '専門用語の適切性        ',
                'contextual_adaptation': '文脈適応性              ',
                'information_completeness': '情報の完全性            '
            }
            
            for criterion, name in criteria_names.items():
                stats = result['statistics'][criterion]
                if stats:
                    print(f"  {name}: 中央値={stats['median']}, 平均={stats['mean']:.1f}, 標準偏差={stats['stdev']:.2f} (スコア: {stats['scores']})")
            
            if total['median'] is not None:
                print(f"  総合得点: 中央値={total['median']}, 平均={total['mean']:.1f}, 標準偏差={total['stdev']:.2f}/100点")
    else:
        # 簡潔表示：ファイル名と中央値の合計のみ
        if total['median'] is not None:
            print(f"{base_name}: {total['median']}/100点")

# JSON出力（オプション）
if args.output_file:
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(aggregated_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n集約結果をJSONで保存しました: {args.output_file}")

if args.verbose:
    print(f"\n処理完了: {len(aggregated_results)}件のファイルグループを集約しました")
