#!/usr/bin/env python3
"""
評価者間比較レポート生成スクリプト

stats.jsonと生成されたグラフを元に、包括的なマークダウンレポートを作成する。
"""

import json
from pathlib import Path
from datetime import datetime

INPUT_JSON = 'stats.json'
PLOTS_DIR = 'plots'
OUTPUT_MD = 'REPORT.md'


def load_data():
    """stats.jsonを読み込む"""
    json_path = Path(__file__).parent / INPUT_JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_table_row(cells, alignment='left'):
    """テーブルの行を整形"""
    if alignment == 'center':
        return '| ' + ' | '.join(str(c).center(15) for c in cells) + ' |'
    return '| ' + ' | '.join(str(c) for c in cells) + ' |'


def generate_executive_summary(data):
    """エグゼクティブサマリーを生成"""
    md = []
    md.append("## エグゼクティブサマリー")
    md.append("")

    metadata = data['metadata']
    decision = data['migration_decision']

    judgment_labels = {
        'possible': '✅ 移行可能',
        'conditional': '⚠️ 条件付き移行可能',
        'impossible': '❌ 移行不可',
    }

    md.append(f"- **分析対象**: {metadata['num_entries']}項目の翻訳評価結果")
    md.append(f"- **評価者**: {', '.join(metadata['evaluators'])}")
    md.append(f"- **移行判定**: {judgment_labels[decision['judgment']]}")
    md.append("")

    # 主な結論
    md.append("### 主な結論")
    md.append("")

    if decision['judgment'] == 'possible':
        md.append("Gemini-2.5-flashからgpt-oss-120bへの完全移行が**可能**です。")
        md.append("主要な評価指標がすべて基準を満たしており、追加の補正なしで代替できます。")
    elif decision['judgment'] == 'conditional':
        md.append("Gemini-2.5-flashからgpt-oss-120bへの**条件付き移行が可能**です。")
        md.append("モデルファミリー別のオフセット補正を適用することで、実用的な代替が可能です。")
    else:
        md.append("Gemini-2.5-flashからgpt-oss-120bへの移行は**推奨できません**。")
        md.append("評価傾向の差が大きすぎるため、別の評価手法を検討する必要があります。")

    md.append("")

    # 主要指標のサマリー
    md.append("### 主要指標")
    md.append("")
    md.append("| 指標 | 値 | 基準 | 判定 |")
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

    md.append(f"| スピアマン順位相関係数 | {spearman:.3f} | ≥0.85 (可), ≥0.70 (条件付き) | {judge_icon(spearman, 0.85, 0.70)} |")
    md.append(f"| 上位10%モデル一致率 | {top10:.1%} | ≥75% (可), ≥60% (条件付き) | {judge_icon(top10, 0.75, 0.60)} |")
    md.append(f"| ±10点範囲内一致率 | {within10:.1%} | ≥70% (可), ≥60% (条件付き) | {judge_icon(within10, 0.70, 0.60)} |")
    md.append(f"| 最大モデルファミリー別バイアス | {decision['max_family_bias']:.1f}点 | ≤15点 (補正容易) | {judge_icon(15 - decision['max_family_bias'], 0, -100)} |")

    md.append("")
    return '\n'.join(md)


def generate_basic_stats(data):
    """基本統計セクションを生成"""
    md = []
    md.append("## 基本統計")
    md.append("")

    md.append("### 評価者ごとの基本統計量")
    md.append("")
    md.append("| 評価者 | 平均 | 中央値 | 標準偏差 | 最小値 | 最大値 | Q25 | Q75 |")
    md.append("|--------|------|--------|----------|--------|--------|-----|-----|")

    basic_stats = data['basic_stats']
    for name, stats in basic_stats.items():
        md.append(f"| {name} | {stats['mean']:.2f} | {stats['median']:.2f} | {stats['std']:.2f} | "
                 f"{stats['min']} | {stats['max']} | {stats['q25']:.2f} | {stats['q75']:.2f} |")

    md.append("")
    md.append("### スコアレンジ別の分布")
    md.append("")
    md.append("| 評価者 | 0-20点 | 21-40点 | 41-60点 | 61-80点 | 81-100点 |")
    md.append("|--------|--------|---------|---------|---------|----------|")

    for name, stats in basic_stats.items():
        ranges = stats['score_ranges']
        md.append(f"| {name} | {ranges['0-20']} | {ranges['21-40']} | {ranges['41-60']} | "
                 f"{ranges['61-80']} | {ranges['81-100']} |")

    md.append("")
    return '\n'.join(md)


def generate_correlation_analysis(data):
    """相関分析セクションを生成"""
    md = []
    md.append("## 相関分析")
    md.append("")

    md.append("![散布図マトリクス](plots/scatter_matrix.png)")
    md.append("")

    md.append("### 評価者間の相関係数")
    md.append("")
    md.append("| ペア | 共通項目数 | ピアソンr | p値 | スピアマンρ | p値 |")
    md.append("|------|-----------|----------|-----|-------------|-----|")

    correlations = data['correlations']
    for pair_name, corr in correlations.items():
        md.append(f"| {corr['pair']} | {corr['num_common']} | {corr['pearson']:.3f} | "
                 f"{corr['pearson_p']:.2e} | {corr['spearman']:.3f} | {corr['spearman_p']:.2e} |")

    md.append("")

    # 相関係数の解釈
    md.append("### 相関係数の解釈")
    md.append("")
    md.append("- **gpt-oss-20b vs gpt-oss-120b**: 非常に高い相関（ρ≈0.91）で、ほぼ同等の評価傾向")
    md.append("- **gemini vs gpt-oss系**: 中程度の相関（ρ≈0.67）で、体系的な差異が存在")
    md.append("")

    return '\n'.join(md)


def generate_agreement_analysis(data):
    """一致度分析セクションを生成"""
    md = []
    md.append("## 一致度分析")
    md.append("")

    md.append("![Bland-Altmanプロット](plots/bland_altman.png)")
    md.append("")

    md.append("### 評価者間の一致度指標")
    md.append("")
    md.append("| ペア | MAE | RMSE | ±5点以内 | ±10点以内 | 上位10%一致率 | 平均差 | 標準偏差 |")
    md.append("|------|-----|------|----------|-----------|---------------|--------|----------|")

    agreement = data['agreement']
    for pair_name, agree in agreement.items():
        md.append(f"| {agree['pair']} | {agree['mae']:.2f} | {agree['rmse']:.2f} | "
                 f"{agree['within_5pts']:.1%} | {agree['within_10pts']:.1%} | "
                 f"{agree['top10_agreement']:.1%} | {agree['mean_diff']:+.2f} | {agree['std_diff']:.2f} |")

    md.append("")

    md.append("![スコア差の分布](plots/score_diff_histogram.png)")
    md.append("")

    return '\n'.join(md)


def generate_systematic_bias_analysis(data):
    """系統的バイアス分析セクションを生成"""
    md = []
    md.append("## 系統的バイアスの分析")
    md.append("")

    md.append("### モデルファミリー別の偏り")
    md.append("")

    md.append("![モデルファミリー別バイアス](plots/model_family_boxplot.png)")
    md.append("")

    md.append("| モデルファミリー | Gemini平均 | GPT-OSS-120B平均 | 差分(Gemini-GPT120B) |")
    md.append("|-----------------|-----------|-----------------|---------------------|")

    family_data = data['systematic_bias']['by_model_family']
    for family, stats in sorted(family_data.items(), key=lambda x: x[1].get('gemini_gpt120b_diff', 0)):
        if 'gemini-2.5-flash' in stats and 'gpt-oss-120b' in stats:
            gemini_mean = stats['gemini-2.5-flash']
            gpt120b_mean = stats['gpt-oss-120b']
            diff = stats.get('gemini_gpt120b_diff', 0)
            md.append(f"| {family} | {gemini_mean:.2f} | {gpt120b_mean:.2f} | {diff:+.2f} |")

    md.append("")

    # 推論レベル別
    md.append("### 推論レベル別の影響")
    md.append("")
    md.append("| 推論レベル | Gemini平均 | GPT-OSS-120B平均 | 差分 |")
    md.append("|-----------|-----------|-----------------|------|")

    level_data = data['systematic_bias']['by_inference_level']
    for level, stats in sorted(level_data.items()):
        if 'gemini-2.5-flash' in stats and 'gpt-oss-120b' in stats:
            md.append(f"| {level} | {stats['gemini-2.5-flash']:.2f} | "
                     f"{stats['gpt-oss-120b']:.2f} | "
                     f"{stats['gemini-2.5-flash'] - stats['gpt-oss-120b']:+.2f} |")

    md.append("")

    # 温度設定別
    md.append("### 温度設定別の影響")
    md.append("")
    md.append("| 温度 | Gemini平均 | GPT-OSS-120B平均 | 差分 |")
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
    """問題ケース分析セクションを生成"""
    md = []
    md.append("## 問題ケースの詳細")
    md.append("")

    problem_cases = data['problem_cases']

    # 乖離が大きいケース
    md.append("### 乖離が大きいケース TOP30")
    md.append("")
    md.append("| 順位 | モデル名 | Geminiスコア | GPT-OSS-120Bスコア | 差分 |")
    md.append("|------|----------|-------------|-------------------|------|")

    for idx, case in enumerate(problem_cases['large_discrepancy'][:30], 1):
        md.append(f"| {idx} | {case['model']} | {case['gemini_score']} | "
                 f"{case['gpt120b_score']} | {case['diff']:+d} |")

    md.append("")

    # 0点評価ケース
    md.append("### 0点評価ケース")
    md.append("")

    if problem_cases['zero_scores']:
        md.append("| モデル名 | 評価者 |")
        md.append("|----------|--------|")

        for case in problem_cases['zero_scores']:
            md.append(f"| {case['model']} | {case['evaluator']} |")

        md.append("")
        md.append("**注意**: qwen3-30b-nt系列がgpt-oss系で0点評価されているのは特に注目すべき問題です。")
    else:
        md.append("0点評価のケースはありません。")

    md.append("")

    # 逆転ケース
    md.append("### 逆転ケース（評価が真逆）")
    md.append("")

    if problem_cases['reversals']:
        md.append("| モデル名 | Geminiスコア | GPT-OSS-120Bスコア | 差分 |")
        md.append("|----------|-------------|-------------------|------|")

        for case in problem_cases['reversals']:
            md.append(f"| {case['model']} | {case['gemini_score']} | "
                     f"{case['gpt120b_score']} | {case['diff']:+d} |")
    else:
        md.append("逆転ケースはありません。")

    md.append("")
    return '\n'.join(md)


def generate_migration_decision(data):
    """移行判定セクションを生成"""
    md = []
    md.append("## 移行判定")
    md.append("")

    decision = data['migration_decision']

    judgment_labels = {
        'possible': '✅ 移行可能',
        'conditional': '⚠️ 条件付き移行可能',
        'impossible': '❌ 移行不可',
    }

    md.append(f"### 判定結果: **{judgment_labels[decision['judgment']]}**")
    md.append("")

    md.append("### 判定基準との照合")
    md.append("")

    for reason in decision['reasons']:
        md.append(f"- {reason}")

    md.append("")

    # 推奨事項
    md.append("### 推奨事項")
    md.append("")

    if decision['judgment'] == 'possible':
        md.append("gpt-oss-120bは Gemini-2.5-flash の代替として使用できます。")
        md.append("")
        md.append("**移行手順**:")
        md.append("1. batch.sh 内の評価モデルを `gpt-oss-120b` に変更")
        md.append("2. 既存の評価結果と比較検証を実施")
        md.append("3. 問題がなければ完全移行")

    elif decision['judgment'] == 'conditional':
        md.append("モデルファミリー別のオフセット補正を適用することで、gpt-oss-120bを代替として使用できます。")
        md.append("")
        md.append("### 補正式")
        md.append("")
        md.append("```python")
        md.append("# モデルファミリー別オフセット補正")
        md.append("def apply_correction(model_name: str, gpt_oss_score: int) -> int:")
        md.append("    family = extract_model_family(model_name)")
        md.append("    ")
        md.append("    # オフセット値 (Gemini平均 - GPT-OSS平均)")
        md.append("    offsets = {")

        # 補正値を計算
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

        md.append("**移行手順**:")
        md.append("1. 上記の補正関数を実装")
        md.append("2. gpt-oss-120bでの評価結果に補正を適用")
        md.append("3. 補正後の結果がGeminiと一致することを確認")
        md.append("4. 問題がなければ補正付きで移行")

    else:
        md.append("gpt-oss-120bは Gemini-2.5-flash の代替として推奨できません。")
        md.append("")
        md.append("**代替案**:")
        md.append("1. より大規模なgpt-ossモデルを試す（もし利用可能なら）")
        md.append("2. 複数の評価者（gpt-oss-20b, gpt-oss-120b）の平均を使用")
        md.append("3. Gemini-2.5-flashを継続使用し、コスト最適化を他の方法で実施")

    md.append("")
    return '\n'.join(md)


def generate_heatmap_section():
    """ヒートマップセクションを生成"""
    md = []
    md.append("## 全項目スコアの俯瞰")
    md.append("")
    md.append("![全716項目ヒートマップ](plots/heatmap.png)")
    md.append("")
    md.append("このヒートマップは全716項目の評価スコアを色で表現したものです。")
    md.append("赤色は高得点、緑色は低得点を示します。")
    md.append("")
    return '\n'.join(md)


def generate_footer(data):
    """フッターを生成"""
    md = []
    md.append("## 詳細データ")
    md.append("")
    md.append(f"- 統計データ: [{INPUT_JSON}]({INPUT_JSON})")
    md.append(f"- グラフ: [{PLOTS_DIR}/]({PLOTS_DIR}/)")
    md.append("")
    md.append("---")
    md.append("")
    md.append(f"生成日時: {data['metadata']['generated_at']}")
    md.append("")
    return '\n'.join(md)


def main():
    """メイン処理"""
    print("=" * 60)
    print("評価者間比較レポート生成")
    print("=" * 60)

    # データ読み込み
    print(f"\n[1] {INPUT_JSON} を読み込み中...")
    data = load_data()
    print(f"  ✓ 読み込み完了")

    # レポート生成
    print(f"\n[2] マークダウンレポートを生成中...")

    md_sections = []

    # ヘッダー
    md_sections.append("# 評価者間比較分析レポート")
    md_sections.append("")
    md_sections.append(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_sections.append("")

    # 各セクション
    md_sections.append(generate_executive_summary(data))
    md_sections.append(generate_basic_stats(data))
    md_sections.append(generate_correlation_analysis(data))
    md_sections.append(generate_agreement_analysis(data))
    md_sections.append(generate_systematic_bias_analysis(data))
    md_sections.append(generate_problem_cases(data))
    md_sections.append(generate_migration_decision(data))
    md_sections.append(generate_heatmap_section())
    md_sections.append(generate_footer(data))

    report_content = '\n'.join(md_sections)

    # ファイル保存
    output_path = Path(__file__).parent / OUTPUT_MD
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"  ✓ レポート生成完了: {output_path}")

    # 統計情報表示
    print(f"\n[3] レポート統計:")
    print(f"  - 総行数: {len(report_content.split(chr(10)))}")
    print(f"  - 総文字数: {len(report_content)}")
    print(f"  - セクション数: {len(md_sections)}")

    print("\n" + "=" * 60)
    print("レポート生成完了")
    print("=" * 60)


if __name__ == '__main__':
    main()
