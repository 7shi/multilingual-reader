#!/usr/bin/env python3
"""
Inter-evaluator comparison report generation script

Creates a comprehensive Markdown report based on stats.json.
"""

import json
from pathlib import Path
from datetime import datetime

INPUT_JSON = 'stats.json'
OUTPUT_MD = 'REPORT.md'


def load_data():
    """Load stats.json"""
    json_path = Path(__file__).parent / INPUT_JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_table_row(cells, alignment='left'):
    """Format a table row"""
    if alignment == 'center':
        return '| ' + ' | '.join(str(c).center(15) for c in cells) + ' |'
    return '| ' + ' | '.join(str(c) for c in cells) + ' |'


def generate_executive_summary(data):
    """Generate the executive summary"""
    md = []
    md.append("## Executive Summary")
    md.append("")

    metadata = data['metadata']
    decision = data['migration_decision']

    judgment_labels = {
        'possible': '✅ Migration possible',
        'conditional': '⚠️ Conditional migration possible',
        'impossible': '❌ Migration not recommended',
    }

    md.append(f"- **Scope of analysis**: translation evaluation results for {metadata['num_entries']} items")
    md.append(f"- **Evaluators**: {', '.join(metadata['evaluators'])}")
    md.append(f"- **Migration decision**: {judgment_labels[decision['judgment']]}")
    md.append("")

    # Key conclusion
    md.append("### Key Conclusion")
    md.append("")

    if decision['judgment'] == 'possible':
        md.append("A full migration from Gemini-2.5-flash to gpt-oss-120b is **possible**.")
        md.append("All key evaluation metrics meet the criteria, so it can serve as a replacement without additional correction.")
    elif decision['judgment'] == 'conditional':
        md.append("A **conditional migration** from Gemini-2.5-flash to gpt-oss-120b is possible.")
        md.append("Applying an offset correction per model family enables a practical replacement.")
    else:
        md.append("Migration from Gemini-2.5-flash to gpt-oss-120b is **not recommended**.")
        md.append("The difference in evaluation tendencies is too large, so an alternative evaluation method should be considered.")

    md.append("")

    # Summary of key metrics
    md.append("### Key Metrics")
    md.append("")
    md.append("| Metric | Value | Criterion | Result |")
    md.append("|------|-----|------|------|")

    spearman = decision['spearman_correlation']
    top10 = decision['top10_agreement']
    within10 = decision['within_10pts_rate']

    def judge_icon(value, threshold_ok, threshold_warn):
        if value >= threshold_ok:
            return "✅"
        elif value >= threshold_warn:
            return "⚠️"
        else:
            return "❌"

    md.append(f"| Spearman rank correlation | {spearman:.3f} | >=0.85 (pass), >=0.70 (conditional) | {judge_icon(spearman, 0.85, 0.70)} |")
    md.append(f"| Top-10% model agreement rate | {top10:.1%} | >=75% (pass), >=60% (conditional) | {judge_icon(top10, 0.75, 0.60)} |")
    md.append(f"| Agreement rate within +/-10 points | {within10:.1%} | >=70% (pass), >=60% (conditional) | {judge_icon(within10, 0.70, 0.60)} |")
    md.append(f"| Max per-model-family bias | {decision['max_family_bias']:.1f} pts | <=15 pts (easily correctable) | {judge_icon(15 - decision['max_family_bias'], 0, -100)} |")

    md.append("")
    return '\n'.join(md)


def generate_basic_stats(data):
    """Generate the basic statistics section"""
    md = []
    md.append("## Basic Statistics")
    md.append("")

    md.append("### Basic Statistics per Evaluator")
    md.append("")
    md.append("| Evaluator | Mean | Median | Std Dev | Min | Max | Q25 | Q75 |")
    md.append("|--------|------|--------|----------|--------|--------|-----|-----|")

    basic_stats = data['basic_stats']
    for name, stats in basic_stats.items():
        md.append(f"| {name} | {stats['mean']:.2f} | {stats['median']:.2f} | {stats['std']:.2f} | "
                 f"{stats['min']} | {stats['max']} | {stats['q25']:.2f} | {stats['q75']:.2f} |")

    md.append("")
    md.append("### Distribution by Score Range")
    md.append("")
    md.append("| Evaluator | 0-20 | 21-40 | 41-60 | 61-80 | 81-100 |")
    md.append("|--------|--------|---------|---------|---------|----------|")

    for name, stats in basic_stats.items():
        ranges = stats['score_ranges']
        md.append(f"| {name} | {ranges['0-20']} | {ranges['21-40']} | {ranges['41-60']} | "
                 f"{ranges['61-80']} | {ranges['81-100']} |")

    md.append("")
    md.append("### Distribution of High-Score Band (95 and above)")
    md.append("")
    md.append("| Evaluator | >=95 | >=96 | >=97 | >=98 | >=99 | 100 |")
    md.append("|--------|----------|----------|----------|----------|----------|-------|")

    for name, stats in basic_stats.items():
        if 'high_score_counts' in stats:
            hsc = stats['high_score_counts']
            md.append(f"| {name} | {hsc['>=95']} | {hsc['>=96']} | {hsc['>=97']} | "
                     f"{hsc['>=98']} | {hsc['>=99']} | {hsc['100']} |")

    md.append("")
    return '\n'.join(md)


def generate_correlation_analysis(data):
    """Generate the correlation analysis section"""
    md = []
    md.append("## Correlation Analysis")
    md.append("")

    md.append("### Correlation Coefficients Between Evaluators")
    md.append("")
    md.append("| Pair | Common Items | Pearson r | p-value | Spearman rho | p-value |")
    md.append("|------|-----------|----------|-----|-------------|-----|")

    correlations = data['correlations']
    for pair_name, corr in correlations.items():
        md.append(f"| {corr['pair']} | {corr['num_common']} | {corr['pearson']:.3f} | "
                 f"{corr['pearson_p']:.2e} | {corr['spearman']:.3f} | {corr['spearman_p']:.2e} |")

    md.append("")

    # Interpretation of correlation coefficients
    md.append("### Interpretation of Correlation Coefficients")
    md.append("")
    md.append("- **gpt-oss-20b vs gpt-oss-120b**: very high correlation (rho≈0.91), nearly equivalent evaluation tendencies")
    md.append("- **gemini vs gpt-oss family**: moderate correlation (rho≈0.67), systematic differences exist")
    md.append("")

    return '\n'.join(md)


def generate_agreement_analysis(data):
    """Generate the agreement analysis section"""
    md = []
    md.append("## Agreement Analysis")
    md.append("")

    md.append("### Agreement Metrics Between Evaluators")
    md.append("")
    md.append("| Pair | MAE | RMSE | Within +/-5 | Within +/-10 | Top-10% Agreement | Mean Diff | Std Dev |")
    md.append("|------|-----|------|----------|-----------|---------------|--------|----------|")

    agreement = data['agreement']
    for pair_name, agree in agreement.items():
        md.append(f"| {agree['pair']} | {agree['mae']:.2f} | {agree['rmse']:.2f} | "
                 f"{agree['within_5pts']:.1%} | {agree['within_10pts']:.1%} | "
                 f"{agree['top10_agreement']:.1%} | {agree['mean_diff']:+.2f} | {agree['std_diff']:.2f} |")

    md.append("")
    return '\n'.join(md)


def generate_systematic_bias_analysis(data):
    """Generate the systematic bias analysis section"""
    md = []
    md.append("## Systematic Bias Analysis")
    md.append("")

    md.append("### Bias by Model Family")
    md.append("")

    md.append("| Model Family | Gemini Mean | GPT-OSS-120B Mean | Diff (Gemini-GPT120B) |")
    md.append("|-----------------|-----------|-----------------|---------------------|")

    family_data = data['systematic_bias']['by_model_family']
    for family, stats in sorted(family_data.items(), key=lambda x: x[1].get('gemini_gpt120b_diff', 0)):
        if 'gemini-2.5-flash' in stats and 'gpt-oss-120b' in stats:
            gemini_mean = stats['gemini-2.5-flash']
            gpt120b_mean = stats['gpt-oss-120b']
            diff = stats.get('gemini_gpt120b_diff', 0)
            md.append(f"| {family} | {gemini_mean:.2f} | {gpt120b_mean:.2f} | {diff:+.2f} |")

    md.append("")

    # By inference level
    md.append("### Impact by Inference Level")
    md.append("")
    md.append("| Inference Level | Gemini Mean | GPT-OSS-120B Mean | Diff |")
    md.append("|-----------|-----------|-----------------|------|")

    level_data = data['systematic_bias']['by_inference_level']
    for level, stats in sorted(level_data.items()):
        if 'gemini-2.5-flash' in stats and 'gpt-oss-120b' in stats:
            md.append(f"| {level} | {stats['gemini-2.5-flash']:.2f} | "
                     f"{stats['gpt-oss-120b']:.2f} | "
                     f"{stats['gemini-2.5-flash'] - stats['gpt-oss-120b']:+.2f} |")

    md.append("")

    # By temperature setting
    md.append("### Impact by Temperature Setting")
    md.append("")
    md.append("| Temperature | Gemini Mean | GPT-OSS-120B Mean | Diff |")
    md.append("|------|-----------|-----------------|------|")

    temp_data = data['systematic_bias']['by_temperature']
    for temp, stats in sorted(temp_data.items()):
        if 'gemini-2.5-flash' in stats and 'gpt-oss-120b' in stats:
            md.append(f"| {temp} | {stats['gemini-2.5-flash']:.2f} | "
                     f"{stats['gpt-oss-120b']:.2f} | "
                     f"{stats['gemini-2.5-flash'] - stats['gpt-oss-120b']:+.2f} |")

    md.append("")
    return '\n'.join(md)


def generate_problem_cases(data):
    """Generate the problem cases analysis section"""
    md = []
    md.append("## Problem Case Details")
    md.append("")

    problem_cases = data['problem_cases']

    # Cases with a large discrepancy
    md.append("### Top 30 Cases with the Largest Discrepancy")
    md.append("")
    md.append("| Rank | Model | Gemini Score | GPT-OSS-120B Score | Diff |")
    md.append("|------|----------|-------------|-------------------|------|")

    for idx, case in enumerate(problem_cases['large_discrepancy'][:30], 1):
        md.append(f"| {idx} | {case['model']} | {case['gemini_score']} | "
                 f"{case['gpt120b_score']} | {case['diff']:+d} |")

    md.append("")

    # Zero-score cases
    md.append("### Zero-Score Cases")
    md.append("")

    if problem_cases['zero_scores']:
        md.append("| Model | Evaluator |")
        md.append("|----------|--------|")

        for case in problem_cases['zero_scores']:
            md.append(f"| {case['model']} | {case['evaluator']} |")

        md.append("")
        md.append("**Note**: it is particularly notable that the qwen3-30b-nt family is scored 0 by the gpt-oss family.")
    else:
        md.append("There are no zero-score cases.")

    md.append("")

    # Reversal cases
    md.append("### Reversal Cases (opposite evaluations)")
    md.append("")

    if problem_cases['reversals']:
        md.append("| Model | Gemini Score | GPT-OSS-120B Score | Diff |")
        md.append("|----------|-------------|-------------------|------|")

        for case in problem_cases['reversals']:
            md.append(f"| {case['model']} | {case['gemini_score']} | "
                     f"{case['gpt120b_score']} | {case['diff']:+d} |")
    else:
        md.append("There are no reversal cases.")

    md.append("")
    return '\n'.join(md)


def generate_migration_decision(data):
    """Generate the migration decision section"""
    md = []
    md.append("## Migration Decision")
    md.append("")

    decision = data['migration_decision']

    judgment_labels = {
        'possible': '✅ Migration possible',
        'conditional': '⚠️ Conditional migration possible',
        'impossible': '❌ Migration not recommended',
    }

    md.append(f"### Decision: **{judgment_labels[decision['judgment']]}**")
    md.append("")

    md.append("### Comparison Against Decision Criteria")
    md.append("")

    for reason in decision['reasons']:
        md.append(f"- {reason}")

    md.append("")

    # Recommendations
    md.append("### Recommendations")
    md.append("")

    if decision['judgment'] == 'possible':
        md.append("gpt-oss-120b can be used as a replacement for Gemini-2.5-flash.")
        md.append("")
        md.append("**Migration steps**:")
        md.append("1. Change the evaluation model in batch.sh to `gpt-oss-120b`")
        md.append("2. Compare against and validate the existing evaluation results")
        md.append("3. Complete the full migration if there are no issues")

    elif decision['judgment'] == 'conditional':
        md.append("Applying an offset correction per model family allows gpt-oss-120b to be used as a replacement.")
        md.append("")
        md.append("### Correction Formula")
        md.append("")
        md.append("```python")
        md.append("# Offset correction per model family")
        md.append("def apply_correction(model_name: str, gpt_oss_score: int) -> int:")
        md.append("    family = extract_model_family(model_name)")
        md.append("    ")
        md.append("    # Offset values (Gemini mean - GPT-OSS mean)")
        md.append("    offsets = {")

        # Compute correction values
        family_data = data['systematic_bias']['by_model_family']
        for family, stats in sorted(family_data.items(), key=lambda x: x[1].get('gemini_gpt120b_diff', 0)):
            if 'gemini_gpt120b_diff' in stats:
                offset = stats['gemini_gpt120b_diff']
                md.append(f"        '{family}': {offset:.1f},")

        md.append("    }")
        md.append("    ")
        md.append("    offset = offsets.get(family, 0)")
        md.append("    corrected_score = gpt_oss_score + offset")
        md.append("    return int(max(0, min(100, corrected_score)))")
        md.append("```")
        md.append("")

        md.append("**Migration steps**:")
        md.append("1. Implement the correction function above")
        md.append("2. Apply the correction to gpt-oss-120b's evaluation results")
        md.append("3. Verify that the corrected results match Gemini")
        md.append("4. Migrate with the correction applied if there are no issues")

    else:
        md.append("gpt-oss-120b is not recommended as a replacement for Gemini-2.5-flash.")
        md.append("")
        md.append("**Alternatives**:")
        md.append("1. Try a larger gpt-oss model (if available)")
        md.append("2. Use the average of multiple evaluators (gpt-oss-20b, gpt-oss-120b)")
        md.append("3. Continue using Gemini-2.5-flash and pursue cost optimization by other means")

    md.append("")
    return '\n'.join(md)


def generate_footer(data):
    """Generate the footer"""
    md = []
    md.append("## Detailed Data")
    md.append("")
    md.append(f"- Statistics data: [{INPUT_JSON}]({INPUT_JSON})")
    md.append("")
    md.append("---")
    md.append("")
    md.append(f"Generated at: {data['metadata']['generated_at']}")
    md.append("")
    return '\n'.join(md)


def main():
    """Main process"""
    print("=" * 60)
    print("Inter-evaluator comparison report generation")
    print("=" * 60)

    # Load data
    print(f"\n[1] Loading {INPUT_JSON}...")
    data = load_data()
    print(f"  ✓ Load complete")

    # Generate report
    print(f"\n[2] Generating Markdown report...")

    md_sections = []

    # Header
    md_sections.append("# Inter-Evaluator Comparison Analysis Report")
    md_sections.append("")
    md_sections.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_sections.append("")

    # Each section
    md_sections.append(generate_executive_summary(data))
    md_sections.append(generate_basic_stats(data))
    md_sections.append(generate_correlation_analysis(data))
    md_sections.append(generate_agreement_analysis(data))
    md_sections.append(generate_systematic_bias_analysis(data))
    md_sections.append(generate_problem_cases(data))
    md_sections.append(generate_migration_decision(data))
    md_sections.append(generate_footer(data))

    report_content = '\n'.join(md_sections)

    # Save file
    output_path = Path(__file__).parent / OUTPUT_MD
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"  ✓ Report generation complete: {output_path}")

    # Display statistics
    print(f"\n[3] Report statistics:")
    print(f"  - Total lines: {len(report_content.split(chr(10)))}")
    print(f"  - Total characters: {len(report_content)}")
    print(f"  - Sections: {len(md_sections)}")

    print("\n" + "=" * 60)
    print("Report generation complete")
    print("=" * 60)


if __name__ == '__main__':
    main()
