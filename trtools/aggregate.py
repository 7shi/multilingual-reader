# Evaluation result aggregation script (median calculation)

import argparse
import json
import os
import re
from statistics import median, mean, stdev
from pathlib import Path

def find_evaluation_groups(files):
    """Search the file list for evaluation file groups"""
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

    complete_groups = {}
    for base_name, runs in groups.items():
        if len(runs) == 3 and all(i in runs for i in [1, 2, 3]):
            complete_groups[base_name] = runs

    return complete_groups

def load_evaluation_data(filepath):
    """Load an evaluation JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def calculate_statistics(evaluation_data_list):
    """Calculate per-criterion statistics from 3 evaluation runs"""
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

    valid_stats = [stat for stat in statistics.values() if stat is not None]
    if len(valid_stats) == 5:
        total_median = sum(stat['median'] for stat in valid_stats)
        total_mean = sum(stat['mean'] for stat in valid_stats)
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
    """Aggregate evaluation results from the file list"""
    groups = find_evaluation_groups(files)
    results = {}

    for base_name, runs in groups.items():
        evaluation_data_list = []
        for run_num in [1, 2, 3]:
            filepath = runs[run_num]
            data = load_evaluation_data(filepath)
            evaluation_data_list.append(data)

        statistics, total_scores = calculate_statistics(evaluation_data_list)

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

def add_parser(subparsers):
    parser = subparsers.add_parser("agg", help="Aggregate the median of evaluation result JSON files")
    parser.add_argument("files", nargs="+", help="Evaluation result JSON files (multiple allowed)")
    parser.add_argument("-o", "--output", dest="output_file", help="Filename to save the aggregated result as JSON")
    parser.add_argument("--verbose", action="store_true", help="Show detailed statistics")
    parser.set_defaults(func=run)
    return parser

def run(args):
    aggregated_results = aggregate_evaluations(args.files)

    for base_name, result in aggregated_results.items():
        total = result['total_scores']

        if args.verbose:
            print(f"\n{base_name}:")
            if result['statistics']:
                criteria_names = {
                    'readability': 'Readability & comprehensibility',
                    'fluency': 'Fluency & naturalness           ',
                    'terminology': 'Terminology appropriateness     ',
                    'contextual_adaptation': 'Contextual adaptation           ',
                    'information_completeness': 'Information completeness        '
                }
                for criterion, name in criteria_names.items():
                    stats = result['statistics'][criterion]
                    if stats:
                        print(f"  {name}: median={stats['median']}, mean={stats['mean']:.1f}, stdev={stats['stdev']:.2f} (scores: {stats['scores']})")
                if total['median'] is not None:
                    print(f"  Total score: median={total['median']}, mean={total['mean']:.1f}, stdev={total['stdev']:.2f}/100")
        else:
            if total['median'] is not None:
                print(f"{base_name}: {total['median']}")

    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            json.dump(aggregated_results, f, ensure_ascii=False, indent=2)
        print(f"\nSaved aggregated result as JSON: {args.output_file}")

    if args.verbose:
        print(f"\nDone: aggregated {len(aggregated_results)} file group(s)")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Aggregate the median of evaluation result JSON files")
    subparsers = parser.add_subparsers()
    add_parser(subparsers)
    args = parser.parse_args(["agg"] + __import__("sys").argv[1:])
    args.func(args)
