#!/usr/bin/env python3
"""
評価者間比較グラフ生成スクリプト

stats.jsonを読み込み、5種類のグラフを生成する。
"""

import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
from scipy import stats as scipy_stats

INPUT_JSON = 'stats.json'
OUTPUT_DIR = 'plots'

# 日本語フォント設定
def setup_japanese_font():
    """日本語フォントを設定"""
    def _set_rcparams_with_font_name(font_name: str) -> None:
        # seaborn/matplotlibのデフォルト設定と衝突しにくいように sans-serif 経由で指定
        plt.rcParams['font.family'] = 'sans-serif'
        current = list(plt.rcParams.get('font.sans-serif', []))
        plt.rcParams['font.sans-serif'] = [font_name] + [f for f in current if f != font_name]

    def _try_addfont(font_path: str) -> None:
        # このuv環境ではシステムフォントを自動検出できないことがあるため、明示登録する
        addfont = getattr(fm.fontManager, 'addfont', None)
        if callable(addfont):
            addfont(font_path)

    # Noto Sans CJK JPを試す
    font_paths = [
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",  # Arch Linux
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",  # macOS
    ]

    for font_path in font_paths:
        if Path(font_path).exists():
            try:
                _try_addfont(font_path)
                font_prop = fm.FontProperties(fname=font_path)
                font_name = font_prop.get_name()
                _set_rcparams_with_font_name(font_name)
                print(f"  日本語フォント設定: {font_path}")
                return
            except Exception as e:
                continue

    # フォールバック: システムの日本語フォント検索
    for font in fm.fontManager.ttflist:
        if 'CJK' in font.name or 'Noto' in font.name or 'Gothic' in font.name:
            try:
                _set_rcparams_with_font_name(font.name)
                print(f"  日本語フォント設定: {font.name}")
                return
            except:
                continue

    print("  警告: 日本語フォントが見つかりません。デフォルトフォントを使用します。")


def load_data():
    """stats.jsonを読み込む"""
    json_path = Path(__file__).parent / INPUT_JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_scores_file(filepath: str):
    """SCORES.txtを再パースして生データを取得"""
    import re
    scores = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = re.search(r'(?:\d+→)?(.+?):\s*(\d+)/100点', line)
            if match:
                model_name = match.group(1).strip()
                score = int(match.group(2))
                scores[model_name] = score
    return scores


def create_scatter_matrix(data, output_dir):
    """散布図マトリクスを生成"""
    print("  散布図マトリクスを生成中...")

    # SCORES.txtファイルから生データを読み込む
    scores_files = {
        'Gemini': '../gemini-2.5-flash/SCORES.txt',
        'GPT-OSS-20B': '../gpt-oss-20b/SCORES.txt',
        'GPT-OSS-120B': '../gpt-oss-120b/SCORES.txt',
    }

    all_scores = {}
    for name, filepath in scores_files.items():
        full_path = Path(__file__).parent / filepath
        all_scores[name] = parse_scores_file(str(full_path))

    # 共通のモデル名
    common_models = set(all_scores['Gemini'].keys())
    for scores in all_scores.values():
        common_models &= set(scores.keys())

    common_models = sorted(common_models)

    # データ配列を作成
    evaluators = ['Gemini', 'GPT-OSS-20B', 'GPT-OSS-120B']
    score_matrix = np.array([
        [all_scores[name][model] for model in common_models]
        for name in evaluators
    ]).T  # 転置して (n_samples, n_features) の形に

    # 3x3のサブプロット
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    fig.suptitle('評価者間スコア相関マトリクス', fontsize=16, fontweight='bold', y=0.995)

    for i in range(3):
        for j in range(3):
            ax = axes[i, j]

            if i == j:
                # 対角線: ヒストグラム
                ax.hist(score_matrix[:, i], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
                ax.set_xlabel('スコア')
                ax.set_ylabel('頻度')
                ax.set_title(f'{evaluators[i]}の分布')
                ax.grid(True, alpha=0.3)

            elif i < j:
                # 上三角: 散布図 + 回帰直線
                x_data = score_matrix[:, j]
                y_data = score_matrix[:, i]

                ax.scatter(x_data, y_data, alpha=0.3, s=10)

                # 回帰直線
                slope, intercept, r_value, p_value, std_err = scipy_stats.linregress(x_data, y_data)
                line_x = np.array([0, 100])
                line_y = slope * line_x + intercept
                ax.plot(line_x, line_y, 'r-', linewidth=2, label=f'y={slope:.2f}x+{intercept:.1f}')

                # ピアソン相関係数を表示
                ax.text(0.05, 0.95, f'r = {r_value:.3f}', transform=ax.transAxes,
                       fontsize=12, verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

                ax.set_xlabel(evaluators[j])
                ax.set_ylabel(evaluators[i])
                ax.set_xlim(0, 100)
                ax.set_ylim(0, 100)
                ax.grid(True, alpha=0.3)
                ax.legend(loc='lower right', fontsize=10)

            else:
                # 下三角: スピアマン順位相関係数のテキスト表示
                x_data = score_matrix[:, j]
                y_data = score_matrix[:, i]

                spearman_r, spearman_p = scipy_stats.spearmanr(x_data, y_data)

                ax.text(0.5, 0.5, f'スピアマン順位相関\nρ = {spearman_r:.3f}\np = {spearman_p:.2e}',
                       transform=ax.transAxes, fontsize=14, ha='center', va='center',
                       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
                ax.set_xlabel(evaluators[j])
                ax.set_ylabel(evaluators[i])
                ax.set_xticks([])
                ax.set_yticks([])

    plt.tight_layout()
    output_path = output_dir / 'scatter_matrix.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ 保存: {output_path}")


def create_bland_altman_plot(data, output_dir):
    """Bland-Altmanプロットを生成"""
    print("  Bland-Altmanプロットを生成中...")

    # SCORES.txtから生データ取得
    scores_files = {
        'gemini-2.5-flash': '../gemini-2.5-flash/SCORES.txt',
        'gpt-oss-20b': '../gpt-oss-20b/SCORES.txt',
        'gpt-oss-120b': '../gpt-oss-120b/SCORES.txt',
    }

    all_scores = {}
    for name, filepath in scores_files.items():
        full_path = Path(__file__).parent / filepath
        all_scores[name] = parse_scores_file(str(full_path))

    # 3ペアを比較
    pairs = [
        ('gemini-2.5-flash', 'gpt-oss-120b', 'Gemini vs GPT-OSS-120B'),
        ('gemini-2.5-flash', 'gpt-oss-20b', 'Gemini vs GPT-OSS-20B'),
        ('gpt-oss-20b', 'gpt-oss-120b', 'GPT-OSS-20B vs GPT-OSS-120B'),
    ]

    fig, axes = plt.subplots(3, 1, figsize=(12, 15))
    fig.suptitle('Bland-Altman プロット (評価者間の一致度)', fontsize=16, fontweight='bold')

    for idx, (name1, name2, title) in enumerate(pairs):
        ax = axes[idx]

        # 共通モデル
        common = set(all_scores[name1].keys()) & set(all_scores[name2].keys())
        common = sorted(common)

        values1 = np.array([all_scores[name1][m] for m in common])
        values2 = np.array([all_scores[name2][m] for m in common])

        # Bland-Altman計算
        mean_values = (values1 + values2) / 2
        diff_values = values1 - values2

        mean_diff = np.mean(diff_values)
        std_diff = np.std(diff_values, ddof=1)
        upper_limit = mean_diff + 1.96 * std_diff
        lower_limit = mean_diff - 1.96 * std_diff

        # プロット
        ax.scatter(mean_values, diff_values, alpha=0.3, s=15)
        ax.axhline(mean_diff, color='blue', linestyle='-', linewidth=2, label=f'平均差: {mean_diff:.2f}')
        ax.axhline(upper_limit, color='red', linestyle='--', linewidth=2, label=f'+1.96SD: {upper_limit:.2f}')
        ax.axhline(lower_limit, color='red', linestyle='--', linewidth=2, label=f'-1.96SD: {lower_limit:.2f}')
        ax.axhline(0, color='gray', linestyle=':', linewidth=1)

        ax.set_xlabel('平均スコア (評価者1 + 評価者2) / 2')
        ax.set_ylabel('スコア差 (評価者1 - 評価者2)')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 100)

    plt.tight_layout()
    output_path = output_dir / 'bland_altman.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ 保存: {output_path}")


def create_score_diff_histogram(data, output_dir):
    """スコア差のヒストグラムを生成"""
    print("  スコア差ヒストグラムを生成中...")

    # SCORES.txtから生データ取得
    gemini_scores = parse_scores_file(str(Path(__file__).parent / '../gemini-2.5-flash/SCORES.txt'))
    gpt120b_scores = parse_scores_file(str(Path(__file__).parent / '../gpt-oss-120b/SCORES.txt'))

    common = set(gemini_scores.keys()) & set(gpt120b_scores.keys())
    diffs = np.array([gemini_scores[m] - gpt120b_scores[m] for m in sorted(common)])

    # ヒストグラム
    fig, ax = plt.subplots(figsize=(12, 8))

    n, bins, patches = ax.hist(diffs, bins=40, color='steelblue', edgecolor='black', alpha=0.7, density=True)

    # 正規分布曲線
    mean_diff = np.mean(diffs)
    std_diff = np.std(diffs, ddof=1)
    x = np.linspace(diffs.min(), diffs.max(), 200)
    y = scipy_stats.norm.pdf(x, mean_diff, std_diff)
    ax.plot(x, y, 'r-', linewidth=2, label=f'正規分布 (μ={mean_diff:.2f}, σ={std_diff:.2f})')

    ax.axvline(0, color='green', linestyle='--', linewidth=2, label='差=0')
    ax.axvline(mean_diff, color='orange', linestyle='-', linewidth=2, label=f'平均差={mean_diff:.2f}')

    ax.set_xlabel('スコア差 (Gemini - GPT-OSS-120B)', fontsize=12)
    ax.set_ylabel('確率密度', fontsize=12)
    ax.set_title('Gemini vs GPT-OSS-120B スコア差の分布', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    # 統計情報テキスト
    info_text = f'サンプル数: {len(diffs)}\n中央値: {np.median(diffs):.2f}\nMAE: {np.mean(np.abs(diffs)):.2f}'
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=11,
           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    plt.tight_layout()
    output_path = output_dir / 'score_diff_histogram.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ 保存: {output_path}")


def create_model_family_boxplot(data, output_dir):
    """モデルファミリー別ボックスプロットを生成"""
    print("  モデルファミリー別ボックスプロットを生成中...")

    # stats.jsonから系統的バイアスデータを取得
    family_data = data['systematic_bias']['by_model_family']

    families = []
    diffs = []

    for family, stats_dict in family_data.items():
        if 'gemini_gpt120b_diff' in stats_dict:
            families.append(family)
            diffs.append(stats_dict['gemini_gpt120b_diff'])

    # ソート
    sorted_indices = np.argsort(diffs)
    families = [families[i] for i in sorted_indices]
    diffs = [diffs[i] for i in sorted_indices]

    fig, ax = plt.subplots(figsize=(14, 8))

    colors = ['red' if d > 0 else 'blue' for d in diffs]
    bars = ax.barh(families, diffs, color=colors, alpha=0.7, edgecolor='black')

    ax.axvline(0, color='black', linestyle='-', linewidth=2)
    ax.set_xlabel('平均スコア差 (Gemini - GPT-OSS-120B)', fontsize=12, fontweight='bold')
    ax.set_ylabel('モデルファミリー', fontsize=12, fontweight='bold')
    ax.set_title('モデルファミリー別の評価バイアス', fontsize=14, fontweight='bold')
    ax.grid(True, axis='x', alpha=0.3)

    # 凡例
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', alpha=0.7, label='Geminiが厳しい'),
        Patch(facecolor='blue', alpha=0.7, label='GPT-OSSが厳しい')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11)

    plt.tight_layout()
    output_path = output_dir / 'model_family_boxplot.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ 保存: {output_path}")


def create_heatmap(data, output_dir):
    """全716項目のヒートマップを生成"""
    print("  ヒートマップを生成中...")

    # SCORES.txtから生データ取得
    scores_files = {
        'Gemini': '../gemini-2.5-flash/SCORES.txt',
        'GPT-OSS-20B': '../gpt-oss-20b/SCORES.txt',
        'GPT-OSS-120B': '../gpt-oss-120b/SCORES.txt',
    }

    all_scores = {}
    for name, filepath in scores_files.items():
        full_path = Path(__file__).parent / filepath
        all_scores[name] = parse_scores_file(str(full_path))

    # 共通モデル
    common_models = set(all_scores['Gemini'].keys())
    for scores in all_scores.values():
        common_models &= set(scores.keys())

    common_models = sorted(common_models)

    # ヒートマップ用データ作成
    evaluators = ['Gemini', 'GPT-OSS-20B', 'GPT-OSS-120B']
    heatmap_data = np.array([
        [all_scores[name][model] for name in evaluators]
        for model in common_models
    ])

    fig, ax = plt.subplots(figsize=(10, 40))

    im = ax.imshow(heatmap_data, aspect='auto', cmap='RdYlGn', vmin=0, vmax=100)

    ax.set_xticks(range(len(evaluators)))
    ax.set_xticklabels(evaluators, fontsize=12, fontweight='bold')

    # モデル名は多すぎるので、100項目ごとにラベルを表示
    step = max(1, len(common_models) // 50)
    ax.set_yticks(range(0, len(common_models), step))
    ax.set_yticklabels([common_models[i] for i in range(0, len(common_models), step)], fontsize=6)

    ax.set_xlabel('評価者', fontsize=14, fontweight='bold')
    ax.set_ylabel('モデル名', fontsize=14, fontweight='bold')
    ax.set_title(f'全{len(common_models)}項目のスコアヒートマップ', fontsize=16, fontweight='bold')

    # カラーバー
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('スコア (0-100点)', fontsize=12, fontweight='bold')

    plt.tight_layout()
    output_path = output_dir / 'heatmap.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ 保存: {output_path}")


def main():
    """メイン処理"""
    print("=" * 60)
    print("評価者間比較グラフ生成")
    print("=" * 60)

    # 日本語フォント設定
    print("\n[1] 日本語フォントを設定中...")
    setup_japanese_font()

    # データ読み込み
    print(f"\n[2] {INPUT_JSON} を読み込み中...")
    data = load_data()
    print(f"  ✓ 読み込み完了")

    # 出力ディレクトリ作成
    output_dir = Path(__file__).parent / OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    print(f"\n[3] 出力ディレクトリ: {output_dir}")

    # グラフ生成
    print("\n[4] グラフ生成中...")
    create_scatter_matrix(data, output_dir)
    create_bland_altman_plot(data, output_dir)
    create_score_diff_histogram(data, output_dir)
    create_model_family_boxplot(data, output_dir)
    create_heatmap(data, output_dir)

    print("\n" + "=" * 60)
    print("グラフ生成完了")
    print("=" * 60)


if __name__ == '__main__':
    main()
