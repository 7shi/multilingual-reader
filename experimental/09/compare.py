"""Compares scores between best.tsv (pre-revision) and SCORES.txt (post-revision)."""

import re

def load_best(path):
    scores = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            lang, score, _, name = parts[0], int(parts[1]), parts[2], parts[3]
            scores[lang] = (score, name)
    return scores

def load_scores(path):
    scores = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r"onde-(\w+): (\d+)", line)
            if m:
                scores[m.group(1)] = int(m.group(2))
    return scores

def main():
    base_dir = __file__.rsplit("/", 1)[0]
    before = load_best(f"{base_dir}/best.tsv")
    after = load_scores(f"{base_dir}/SCORES.txt")

    langs = sorted(set(before) | set(after))
    rows = []
    for lang in langs:
        b_score, name = before.get(lang, (None, lang))
        a_score = after.get(lang)
        if b_score is None or a_score is None:
            continue
        diff = a_score - b_score
        rows.append((lang, name, b_score, a_score, diff))

    improved = [r for r in rows if r[4] > 0]
    degraded = [r for r in rows if r[4] < 0]
    unchanged = [r for r in rows if r[4] == 0]

    lang_w = max(len(r[0]) for r in rows)
    name_w = max(len(r[1]) for r in rows)
    b_w    = max(len(str(r[2])) for r in rows)
    a_w    = max(len(str(r[3])) for r in rows)
    d_w    = max(len(f"{r[4]:+d}") for r in rows)

    print("# Revision Score Comparison (Pre-revision vs Post-revision)")
    print()
    print("## Sorted by language code")
    print()
    print("| Lang | Language | Pre | Post | Diff |")
    print("|---|---|---:|---:|---:|")
    for lang, name, b, a, d in rows:
        ds = f"{d:+d}" if d != 0 else "0"
        print(f"| {lang:<{lang_w}} | {name:<{name_w}} | {b:>{b_w}} | {a:>{a_w}} | {ds:>{d_w}} |")

    print()
    if rows:
        diffs = [r[4] for r in rows]
        avg = sum(diffs) / len(diffs)
        print(f"Improved: **{len(improved)}** languages / Degraded: **{len(degraded)}** languages / Unchanged: **{len(unchanged)}** languages  ")
        print(f"Average change: **{avg:+.1f}** points / Max improvement: **+{max(diffs)}** points / Max degradation: **{min(diffs)}** points")

    print()
    print("## Sorted descending by post-revision score")
    print()
    print("| Lang | Language | Pre | **Post** | Diff |")
    print("|---|---|---:|---:|---:|")
    for lang, name, b, a, d in sorted(rows, key=lambda x: (-x[3], x[0])):
        ds = f"{d:+d}" if d != 0 else "0"
        print(f"| {lang:<{lang_w}} | {name:<{name_w}} | {b:>{b_w}} | **{a:>{a_w}}** | {ds:>{d_w}} |")

    print()
    print("## Breakdown by 5-point buckets")
    print()
    buckets = {}
    zeros = []
    for lang, name, b, a, d in rows:
        if d == 0:
            zeros.append(name)
        elif d > 0:
            buckets.setdefault(((d - 1) // 5) * 5 + 1, []).append((name, d))
        else:
            buckets.setdefault((d // 5) * 5, []).append((name, d))

    label_w = max(
        (len(f"+{k}～+{k+4}") if k > 0 else len(f"{k}～{k+4}") for k in buckets),
        default=0,
    )
    label_w = max(label_w, len("±0"))

    print("| Range | Languages |")
    print("|---|---|")
    for key in sorted(buckets, reverse=True):
        lo, hi = key, key + 4
        label = f"+{lo}～+{hi}" if lo > 0 else f"{lo}～{hi}"
        entries = ", ".join(f"{n} ({d:+d})" for n, d in sorted(buckets[key], key=lambda x: -x[1]))
        print(f"| {label:<{label_w}} | {entries} |")
        if key == 1 and zeros:
            print(f"| {'±0':<{label_w}} | {', '.join(sorted(zeros))} |")
    if zeros and 1 not in buckets:
        print(f"| {'±0':<{label_w}} | {', '.join(sorted(zeros))} |")

    print()
    print("## Languages where revision was effective (diff +6 or more)")
    print()
    effective = sorted([(n, a, d) for _, n, _, a, d in rows if d >= 6], key=lambda x: (-x[1], x[0]))
    print("- " + ", ".join(f"{n} ({a}:{d:+d})" for n, a, d in effective))

if __name__ == "__main__":
    main()
