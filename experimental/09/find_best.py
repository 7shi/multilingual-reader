#!/usr/bin/env python3
"""各言語の最高得点翻訳を探してTSV（言語コード・得点・ファイルパス・言語名）を標準出力する。"""
import re
from pathlib import Path

from trtools.language import LANG_NAMES


def main():
    base = Path("examples/tr/onde")
    best: dict[str, tuple[int, Path]] = {}

    for model_dir in sorted(base.iterdir()):
        if not model_dir.is_dir():
            continue
        scores_file = model_dir / "SCORES.txt"
        if not scores_file.exists():
            continue

        for line in scores_file.read_text().splitlines():
            m = re.match(r"onde-(\w+): (\d+)", line)
            if not m:
                continue
            code, score = m.group(1), int(m.group(2))

            tr_file = model_dir / "tr" / f"onde-{code}.txt"
            if not tr_file.exists():
                continue

            if code not in best or score > best[code][0]:
                best[code] = (score, tr_file)

    for code in sorted(best):
        score, path = best[code]
        lang_name = LANG_NAMES.get(code, code)
        print(f"{code}\t{score}\t{path}\t{lang_name}")


if __name__ == "__main__":
    main()
