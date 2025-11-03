#!/usr/bin/env python3
"""
SCORES.mdの表をREADME.mdに自動的に同期するスクリプト

アルゴリズム:
1. SCORES.mdの表をヘッダ行をキーとしてdictに格納
2. README.mdを行ごとに走査して、表のヘッダが検出されればdictからマッチング
"""

from pathlib import Path


def extract_tables_from_scores(content: str) -> dict[str, list[str]]:
    """
    SCORES.mdから表を抽出し、ヘッダ行をキーとしてdictに格納する

    キーが重複する場合は最初のものだけを保持する

    Returns:
        {ヘッダ行: [表の全行（ヘッダ、区切り、データ行）]}
    """
    lines = content.split('\n')
    tables = {}
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # 表のヘッダ行を検出（| で始まる行）
        if line.startswith('|'):
            header_line = line
            table_lines = [header_line]
            i += 1

            # 表の残りの行を収集（| で始まる行が続く限り）
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith('|'):
                    table_lines.append(next_line)
                    i += 1
                elif next_line == '':
                    # 空行は表の終わりの可能性があるが、次の行もチェック
                    i += 1
                    break
                else:
                    # 表でない行が来たら表終了
                    break

            # ヘッダ行をキーとして表を保存（重複時は最初のものを保持）
            if header_line not in tables:
                tables[header_line] = table_lines
        else:
            i += 1

    return tables


def sync_readme_with_scores(readme_content: str, tables_dict: dict[str, list[str]]) -> str:
    """
    README.mdの内容を走査し、表のヘッダが見つかったらSCORES.mdの表で置き換える
    """
    lines = readme_content.split('\n')
    result = []
    i = 0
    table_count = 0
    matched_count = 0

    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()

        # 表のヘッダ行を検出
        if line_stripped.startswith('|'):
            table_count += 1
            header_preview = line_stripped[:60] + '...' if len(line_stripped) > 60 else line_stripped

            if line_stripped in tables_dict:
                # マッチした場合
                matched_count += 1
                print(f"  ✓ 表 #{table_count}: マッチしました")
                print(f"    ヘッダ: {header_preview}")

                # SCORES.mdから対応する表を取得
                new_table = tables_dict[line_stripped]
                result.extend(new_table)
                i += 1

                # README.mdの古い表をスキップ
                while i < len(lines):
                    next_line = lines[i].strip()
                    if next_line.startswith('|'):
                        i += 1
                    elif next_line == '':
                        # 空行も追加してスキップ
                        result.append('')
                        i += 1
                        break
                    else:
                        # 表でない行が来たら終了
                        break
            else:
                # マッチしなかった場合
                print(f"  × 表 #{table_count}: マッチしませんでした（そのまま保持）")
                print(f"    ヘッダ: {header_preview}")

                # 通常の行はそのまま追加
                result.append(line)
                i += 1
        else:
            # 通常の行はそのまま追加
            result.append(line)
            i += 1

    print(f"\n  合計: {table_count} 個の表を検出、{matched_count} 個を更新しました")
    return '\n'.join(result)


def main():
    # ファイルパス
    script_dir = Path(__file__).parent
    scores_path = script_dir / 'SCORES.md'
    readme_path = script_dir / 'README.md'

    # 存在確認
    if not scores_path.exists():
        print(f"エラー: {scores_path} が見つかりません")
        return 1

    if not readme_path.exists():
        print(f"エラー: {readme_path} が見つかりません")
        return 1

    # ファイル読み込み
    scores_content = scores_path.read_text(encoding='utf-8')
    readme_content = readme_path.read_text(encoding='utf-8')

    # SCORES.mdから表を抽出
    print("SCORES.mdから表を抽出しています...")
    tables_dict = extract_tables_from_scores(scores_content)
    print(f"  {len(tables_dict)} 個の表を検出しました")

    # README.mdを更新
    print("README.mdの表を更新しています...")
    updated_content = sync_readme_with_scores(readme_content, tables_dict)

    # README.mdに書き込み
    readme_path.write_text(updated_content, encoding='utf-8')
    print("完了しました！")

    return 0


if __name__ == '__main__':
    exit(main())
