#!/usr/bin/env python3
"""Script to generate SCORES.md from SCORES.txt

Key design points:
1. Fully data-driven
   - Model names and test configurations are all auto-extracted from SCORES.txt
   - No hardcoding (decisions are based only on checking whether data exists)

2. Table generation
   - By reasoning level (-r 0-4): only shows models that have -r 0-4 data
   - Levels 0/1/2: dynamically extracts the models and configs that have data for each level
   - Verifying the translation-improvement effect: compares 0-xx and 2-xx data
   - Investigating the impact of structured output: compares 0-xx/1-xx against tr4/tr6
   - Free-form reasoning comparison: compares tr5 and tr6

3. Flag handling ((t), (nt), etc.)
   - Tables: shown as a separate row for the flagged model
   - Practical-config list: shown with the flag, but sorted by base model name

4. Per-model practical-config list (each model's top 3 entries scoring 85+)
   - Sort order: descending by the base model name's highest score (flags are ignored)
   - Display: shown with the flagged model name
   - Within each model: only the top 3 entries by descending score are shown
   - Same model, same score: configs are joined with commas

5. Bold display of the maximum value
   - The maximum score in each table row is shown in bold
"""

import re

def natural_sort_key(text):
    """Key generation function for natural-order sorting

    Converts a string into a list of characters and numbers, treating the numeric
    parts as integers. This makes "a2" sort before "a11".

    Wrapping each element as a (type, value) tuple avoids comparison errors between
    different types. Numbers are stored as (0, int_value), strings as (1, str_value).

    Example:
        "gemma2-9b" -> [(1, "gemma"), (0, 2), (1, "-"), (0, 9), (1, "b")]
        "qwen3-30b" -> [(1, "qwen"), (0, 3), (1, "-"), (0, 30), (1, "b")]
        "a2" -> [(1, "a"), (0, 2)]
        "a11" -> [(1, "a"), (0, 11)]

    Args:
        text: the string to sort

    Returns:
        a list of tuples (the comparison key)
    """
    parts = []
    for part in re.split(r'(\d+)', text):
        if part:
            if part.isdigit():
                # Numbers are stored with priority 0 as an integer value
                parts.append((0, int(part)))
            else:
                # Strings are stored with priority 1 as a string value
                parts.append((1, part))
    return parts

def parse_test_name(test_name):
    """Parse a test name to extract the model name and test type"""
    # Example patterns:
    # gemma2-9b-0 -> model: gemma2-9b, type: -r, variant: 0
    # gemma2-9b-0-05 -> model: gemma2-9b, type: 0-, history: 05
    # gemma2-9b-1-05 -> model: gemma2-9b, type: 1-, history: 05
    # gemma2-9b-tr4-05 -> model: gemma2-9b, type: tr4-, history: 05
    # qwen3-4b-0-t-05 -> model: qwen3-4b, type: 0-, history: 05, flag: t
    # qwen3-30b-tr4-nt-05 -> model: qwen3-30b, type: tr4-, history: 05, flag: nt
    # llama4-scout-0 -> model: llama4-scout, type: -r, variant: 0

    parts = test_name.split('-')

    # Search from the end for known suffix patterns
    # Identify where the suffix begins
    suffix_start = len(parts)

    # Check parts in reverse order starting from the end
    i = len(parts) - 1
    while i >= 0:
        part = parts[i]

        # Numeric pattern (05, 10, 15, 20, 25, 0-4, etc.)
        if part in ['05', '10', '15', '20', '25', '0', '1', '2', '3', '4']:
            suffix_start = i
            i -= 1
            continue

        # a/b suffix
        if part in ['a', 'b'] and i > 0:
            suffix_start = i
            i -= 1
            continue

        # Flags (t, nt)
        if part in ['t', 'nt'] and i > 0:
            suffix_start = i
            i -= 1
            continue

        # tr4/tr5/tr6
        if part in ['tr4', 'tr5', 'tr6'] and i > 0:
            suffix_start = i
            i -= 1
            continue

        # Anything else is part of the model name
        break

    # Extract the model name
    if suffix_start == 0:
        return None

    model_name = '-'.join(parts[:suffix_start])
    remaining = parts[suffix_start:]

    if not model_name or not remaining:
        return None

    # Parse the remaining parts
    test_type = None
    history = None
    flags = []

    i = 0
    while i < len(remaining):
        part = remaining[i]

        # -r 0-4 pattern
        if part in ['0', '1', '2', '3', '4'] and i == 0:
            test_type = '-r'
            variant = part
            i += 1
            # Check whether the next part is the nt flag
            if i < len(remaining) and remaining[i] == 'nt':
                flags.append('nt')
                i += 1
            # Check whether the next part is the t flag
            if i < len(remaining) and remaining[i] == 't':
                flags.append('t')
                i += 1
            # Check whether the next part is history
            if i < len(remaining) and remaining[i] in ['05', '10', '15', '20', '25']:
                history = remaining[i]
                test_type = f"{variant}-"
                i += 1
                # Check whether the next part is a/b
                if i < len(remaining) and remaining[i] in ['a', 'b']:
                    history += f"-{remaining[i]}"
                    i += 1
            else:
                history = variant
        # tr4/tr5/tr6 pattern
        elif part in ['tr4', 'tr5', 'tr6']:
            test_type = f"{part}-"
            i += 1
            # Check the nt flag
            if i < len(remaining) and remaining[i] == 'nt':
                flags.append('nt')
                i += 1
            # history
            if i < len(remaining) and remaining[i] in ['05', '10', '15', '20', '25']:
                history = remaining[i]
                i += 1
        # t flag (0-t-05 pattern)
        elif part == 't':
            flags.append('t')
            i += 1
        else:
            i += 1

    return {
        'model': model_name,
        'type': test_type,
        'history': history,
        'flags': flags
    }

def parse_scores(scores_file):
    """Parse SCORES.txt"""
    all_scores = {}

    with open(scores_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            match = re.match(r'^(.+?):\s*(\d+)$', line)
            if match:
                test_name = match.group(1)
                score = int(match.group(2))
                all_scores[test_name] = score

    return all_scores

def extract_models_from_scores(all_scores):
    """Extract the list of model names from the score data"""
    models_set = set()

    for test_name in all_scores.keys():
        parsed = parse_test_name(test_name)
        if parsed and parsed['model']:
            models_set.add(parsed['model'])

    return sorted(models_set, key=natural_sort_key)

def get_test_configs_by_pattern(all_scores, pattern_type):
    """Extract the test configs for a specific pattern"""
    configs_set = set()

    for test_name in all_scores.keys():
        parsed = parse_test_name(test_name)
        if not parsed:
            continue

        # Extract configs according to the pattern type
        if pattern_type == '-r':
            # -r 0-4 pattern
            if parsed['type'] == '-r' and parsed['history'] in ['0', '1', '2', '3', '4']:
                configs_set.add(parsed['history'])
        elif pattern_type.startswith('level-'):
            # Per-level pattern (0-05, 1-10, etc.)
            level = pattern_type.split('-')[1]
            if parsed['type'] == f"{level}-" and parsed['history']:
                configs_set.add(parsed['history'])
        elif pattern_type.startswith('tr'):
            # tr4, tr5, tr6 pattern
            tr_num = pattern_type[2:]
            if parsed['type'] == f"tr{tr_num}-" and parsed['history']:
                configs_set.add(parsed['history'])

    return sorted(configs_set, key=natural_sort_key)

def has_flag_variant(all_scores, model_name, flag, pattern_prefix=''):
    """Check whether the data contains a specific model and flag combination"""
    for test_name in all_scores.keys():
        if not test_name.startswith(f"{model_name}-"):
            continue
        if pattern_prefix and not pattern_prefix in test_name:
            continue
        parsed = parse_test_name(test_name)
        if parsed and flag in parsed.get('flags', []):
            return True
    return False

def get_model_display_name(model_name, flags):
    """Generate the model display name (with flags)"""
    if flags:
        return f"{model_name} ({','.join(flags)})"
    return model_name

def generate_table(f, title, models, test_configs, all_scores, column_headers=None):
    """Generate a table

    Args:
        f: the output file
        title: the table title
        models: list of model info
        test_configs: list of test configs (used with the pattern)
        all_scores: scores dict
        column_headers: column headers (uses test_configs if omitted)
    """
    if title:
        f.write(f"### {title}\n\n")

    # Use test_configs if column_headers is not specified
    if column_headers is None:
        column_headers = test_configs

    # Header
    f.write("| Model |")
    for header in column_headers:
        f.write(f" {header} |")
    f.write("\n")

    f.write("|:---|")
    for _ in column_headers:
        f.write(":---:|")
    f.write("\n")

    # Data rows
    for model_info in models:
        model_name = model_info['model']
        flags = model_info.get('flags', [])
        display_name = get_model_display_name(model_name, flags)

        f.write(f"| **{display_name}** |")

        max_score = -1
        scores_in_row = []

        # First collect all scores to find the maximum
        for config in test_configs:
            test_name = model_info['pattern'].format(config=config)
            score = all_scores.get(test_name)
            scores_in_row.append(score)
            if score is not None and score > max_score:
                max_score = score

        # Output the scores (bolding the maximum)
        for score in scores_in_row:
            if score is None:
                f.write(" - |")
            elif score == max_score and max_score >= 0:
                f.write(f" **{score}** |")
            else:
                f.write(f" {score} |")
        f.write("\n")

    f.write("\n")

def generate_markdown(all_scores, output_file, practical_threshold=90, highlight_threshold=96):
    """Generate Markdown in the same format as SCORES.md.orig"""

    # Auto-extract model names and test configs
    all_models = extract_models_from_scores(all_scores)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Local LLM Translation Experiment\n\n")

        # System design and experiment scores by reasoning level
        f.write("## Reasoning-Level System Design and Experimental Scores\n\n")

        # Extract only the models that have -r 0-4 data
        models_with_r = []
        for model in all_models:
            # Check whether any -r 0-4 data exists (regular version)
            has_r_data = False
            for i in range(5):
                if f"{model}-{i}" in all_scores:
                    has_r_data = True
                    break
            if has_r_data:
                models_with_r.append({'model': model, 'pattern': f'{model}-{{config}}'})

            # Check whether any -r 0-4 data exists (nt version)
            has_nt_data = False
            for i in range(5):
                if f"{model}-{i}-nt" in all_scores:
                    has_nt_data = True
                    break
            if has_nt_data:
                models_with_r.append({'model': model, 'flags': ['nt'], 'pattern': f'{model}-{{config}}-nt'})

        generate_table(f, "", models_with_r, ['0', '1', '2', '3', '4'], all_scores)

        # Dynamically generate the tables for levels 0, 1, and 2
        for level, title in [('0', 'Level 0: Direct Translation'), ('1', 'Level 1: Translation with Reasoning'), ('2', 'Level 2: Two-Stage Translation')]:
            f.write(f"### {title}\n\n")

            # Extract the test configs for this level
            configs_set = set()
            for test_name in all_scores.keys():
                parsed = parse_test_name(test_name)
                if parsed and parsed['type'] == f"{level}-" and parsed['history']:
                    # Handle history that includes an a/b suffix
                    configs_set.add(parsed['history'])

            # Generate the prefixed column headers
            configs = sorted(configs_set, key=natural_sort_key)
            column_headers = [f"{level}-{config}" for config in configs]

            # Extract the models that have data for this level
            models = []
            for model in all_models:
                # Check whether the regular version has data
                has_data = False
                for config in configs:
                    if f"{model}-{level}-{config}" in all_scores:
                        has_data = True
                        break
                if has_data:
                    models.append({'model': model, 'pattern': f'{model}-{level}-{{config}}'})

                # Check whether the (nt) variant has data
                has_nt_data = False
                for config in configs:
                    if f"{model}-{level}-nt-{config}" in all_scores:
                        has_nt_data = True
                        break
                if has_nt_data:
                    models.append({'model': model, 'flags': ['nt'], 'pattern': f'{model}-{level}-nt-{{config}}'})

                # Check whether the (t) variant has data
                has_t_data = False
                for config in configs:
                    if f"{model}-{level}-t-{config}" in all_scores:
                        has_t_data = True
                        break
                if has_t_data:
                    models.append({'model': model, 'flags': ['t'], 'pattern': f'{model}-{level}-t-{{config}}'})

                # Check whether the (nt,t) variant has data
                has_nt_t_data = False
                for config in configs:
                    if f"{model}-{level}-nt-t-{config}" in all_scores:
                        has_nt_t_data = True
                        break
                if has_nt_t_data:
                    models.append({'model': model, 'flags': ['nt', 't'], 'pattern': f'{model}-{level}-nt-t-{{config}}'})

            generate_table(f, "", models, configs, all_scores, column_headers)

        # Verifying the translation-improvement effect (level 0 vs level 2)
        f.write("### Verifying the Improvement Effect of Translation (Level 0 vs Level 2)\n\n")

        # Collect the 0-xx and 2-xx configs
        configs_0 = set()
        configs_2 = set()
        for test_name in all_scores.keys():
            parsed = parse_test_name(test_name)
            if parsed and parsed['type'] == '0-' and parsed['history']:
                # Exclude 0-15, 0-25; also exclude plain 0-20 (only 0-20-a, 0-20-b)
                if parsed['history'] not in ['15', '20', '25']:
                    configs_0.add(f"0-{parsed['history']}")
            elif parsed and parsed['type'] == '2-' and parsed['history']:
                # Exclude 2-15, 2-25
                if parsed['history'] not in ['15', '25']:
                    configs_2.add(f"2-{parsed['history']}")

        configs = sorted(configs_0, key=natural_sort_key) + sorted(configs_2, key=natural_sort_key)

        # Header
        f.write("| Model |")
        for config in configs:
            f.write(f" {config} |")
        f.write("\n")
        f.write("|:---|")
        for _ in configs:
            f.write(":---:|")
        f.write("\n")

        # Extract the models and variants that have data
        model_configs = []
        for model in all_models:
            # Regular version
            has_data = any(f"{model}-{config}" in all_scores for config in configs)
            if has_data:
                model_configs.append((model, None))

            # (nt) variant
            has_nt_data = False
            for config in configs:
                nt_config = config.replace('0-', '0-nt-').replace('2-', '2-nt-')
                if f"{model}-{nt_config}" in all_scores:
                    has_nt_data = True
                    break
            if has_nt_data:
                model_configs.append((model, 'nt'))

        for model_base, flag_variant in model_configs:
            display_name = f"{model_base} (nt)" if flag_variant == 'nt' else model_base
            f.write(f"| **{display_name}** |")

            max_score = -1
            scores_in_row = []

            for config in configs:
                if flag_variant == 'nt':
                    # Insert nt- after the 0- or 2- in the config
                    nt_config = config.replace('0-', '0-nt-').replace('2-', '2-nt-')
                    test_name = f"{model_base}-{nt_config}"
                else:
                    test_name = f"{model_base}-{config}"

                score = all_scores.get(test_name)
                scores_in_row.append(score)
                if score is not None and score > max_score:
                    max_score = score

            # Output the scores
            for score in scores_in_row:
                if score is None:
                    f.write(" - |")
                elif score == max_score and max_score >= 0:
                    f.write(f" **{score}** |")
                else:
                    f.write(f" {score} |")
            f.write("\n")

        f.write("\n")

        # Investigating the impact of structured output on direct translation (level 0 vs tr4)
        f.write("### Investigating the Impact of Structured Output on Direct Translation (Level 0 vs tr4)\n\n")

        # Collect the 0-xx and tr4-xx configs
        configs_0 = set()
        configs_tr4 = set()
        for test_name in all_scores.keys():
            parsed = parse_test_name(test_name)
            if parsed and parsed['type'] == '0-' and parsed['history']:
                # Exclude 0-15, 0-25; also exclude plain 0-20 (only 0-20-a, 0-20-b)
                if parsed['history'] not in ['15', '20', '25']:
                    configs_0.add(f"0-{parsed['history']}")
            elif parsed and parsed['type'] == 'tr4-' and parsed['history']:
                # Exclude tr4-15, tr4-25
                if parsed['history'] not in ['15', '25']:
                    configs_tr4.add(f"tr4-{parsed['history']}")

        configs = sorted(configs_0, key=natural_sort_key) + sorted(configs_tr4, key=natural_sort_key)

        # Header
        f.write("| Model |")
        for config in configs:
            f.write(f" {config} |")
        f.write("\n")
        f.write("|:---|")
        for _ in configs:
            f.write(":---:|")
        f.write("\n")

        # Extract the models and variants that have data
        model_configs = []
        for model in all_models:
            # Regular version
            has_data = any(f"{model}-{config}" in all_scores for config in configs)
            if has_data:
                model_configs.append((model, None))

            # (nt) variant
            has_nt_data = False
            for config in configs:
                if config.startswith('tr4-'):
                    parts = config.split('-')
                    test_name = f"{model}-{parts[0]}-nt-{parts[1]}"
                    if test_name in all_scores:
                        has_nt_data = True
                        break
            if has_nt_data:
                model_configs.append((model, 'nt'))

        for model_base, flag_variant in model_configs:
            display_name = f"{model_base} (nt)" if flag_variant == 'nt' else model_base
            f.write(f"| **{display_name}** |")

            max_score = -1
            scores_in_row = []

            for config in configs:
                # nt handling differs between 0-xx and tr4-xx
                if config.startswith('0-'):
                    if flag_variant == 'nt':
                        # 0-05 -> 0-nt-05
                        nt_config = config.replace('0-', '0-nt-')
                        test_name = f"{model_base}-{nt_config}"
                    else:
                        test_name = f"{model_base}-{config}"
                    score = all_scores.get(test_name)
                else:  # tr4-xx
                    if flag_variant == 'nt':
                        # tr4-05 -> tr4-nt-05
                        parts = config.split('-')
                        test_name = f"{model_base}-{parts[0]}-nt-{parts[1]}"
                    else:
                        test_name = f"{model_base}-{config}"
                    score = all_scores.get(test_name)

                scores_in_row.append(score)
                if score is not None and score > max_score:
                    max_score = score

            # Output the scores
            for score in scores_in_row:
                if score is None:
                    f.write(" - |")
                elif score == max_score and max_score >= 0:
                    f.write(f" **{score}** |")
                else:
                    f.write(f" {score} |")
            f.write("\n")

        f.write("\n")

        # Investigating the impact of structured output on reasoning-based translation (level 1 vs tr6)
        f.write("### Investigating the Impact of Structured Output on Translation with Reasoning (Level 1 vs tr6)\n\n")

        # Collect the 1-xx and tr6-xx configs
        configs_1 = set()
        configs_tr6 = set()
        for test_name in all_scores.keys():
            parsed = parse_test_name(test_name)
            if parsed and parsed['type'] == '1-' and parsed['history']:
                # Exclude 1-15, 1-25
                if parsed['history'] not in ['15', '25']:
                    configs_1.add(f"1-{parsed['history']}")
            elif parsed and parsed['type'] == 'tr6-' and parsed['history']:
                # Exclude tr6-15, tr6-25
                if parsed['history'] not in ['15', '25']:
                    configs_tr6.add(f"tr6-{parsed['history']}")

        configs = sorted(configs_1, key=natural_sort_key) + sorted(configs_tr6, key=natural_sort_key)

        # Header
        f.write("| Model |")
        for config in configs:
            f.write(f" {config} |")
        f.write("\n")
        f.write("|:---|")
        for _ in configs:
            f.write(":---:|")
        f.write("\n")

        # Extract the models and variants that have data
        model_configs = []
        for model in all_models:
            # Regular version
            has_data = any(f"{model}-{config}" in all_scores for config in configs)
            if has_data:
                model_configs.append((model, None))

            # (nt) variant
            has_nt_data = False
            for config in configs:
                if config.startswith('tr6-'):
                    parts = config.split('-')
                    test_name = f"{model}-{parts[0]}-nt-{parts[1]}"
                    if test_name in all_scores:
                        has_nt_data = True
                        break
            if has_nt_data:
                model_configs.append((model, 'nt'))

        for model_base, flag_variant in model_configs:
            display_name = f"{model_base} (nt)" if flag_variant == 'nt' else model_base
            f.write(f"| **{display_name}** |")

            max_score = -1
            scores_in_row = []

            for config in configs:
                # nt handling differs between 1-xx and tr6-xx
                if config.startswith('1-'):
                    if flag_variant == 'nt':
                        # 1-05 -> 1-nt-05
                        nt_config = config.replace('1-', '1-nt-')
                        test_name = f"{model_base}-{nt_config}"
                    else:
                        test_name = f"{model_base}-{config}"
                    score = all_scores.get(test_name)
                else:  # tr6-xx
                    if flag_variant == 'nt':
                        # tr6-05 -> tr6-nt-05
                        parts = config.split('-')
                        test_name = f"{model_base}-{parts[0]}-nt-{parts[1]}"
                    else:
                        test_name = f"{model_base}-{config}"
                    score = all_scores.get(test_name)

                scores_in_row.append(score)
                if score is not None and score > max_score:
                    max_score = score

            # Output the scores
            for score in scores_in_row:
                if score is None:
                    f.write(" - |")
                elif score == max_score and max_score >= 0:
                    f.write(f" **{score}** |")
                else:
                    f.write(f" {score} |")
            f.write("\n")

        f.write("\n")

        # Free-form reasoning comparison (tr5 vs tr6)
        f.write("### Free-Form Reasoning Comparison (tr5 vs tr6)\n\n")

        # Collect the tr5-xx and tr6-xx configs
        configs_tr5 = set()
        configs_tr6 = set()
        for test_name in all_scores.keys():
            parsed = parse_test_name(test_name)
            if parsed and parsed['type'] == 'tr5-' and parsed['history']:
                configs_tr5.add(f"tr5-{parsed['history']}")
            elif parsed and parsed['type'] == 'tr6-' and parsed['history']:
                configs_tr6.add(f"tr6-{parsed['history']}")

        configs = sorted(configs_tr5, key=natural_sort_key) + sorted(configs_tr6, key=natural_sort_key)

        # Header
        f.write("| Model |")
        for config in configs:
            f.write(f" {config} |")
        f.write("\n")
        f.write("|:---|")
        for _ in configs:
            f.write(":---:|")
        f.write("\n")

        # Extract the models and variants that have data
        model_configs = []
        for model in all_models:
            # Regular version
            has_data = any(f"{model}-{config}" in all_scores for config in configs)
            if has_data:
                model_configs.append((model, None))

            # (nt) variant
            has_nt_data = False
            for config in configs:
                parts = config.split('-')
                if len(parts) == 2:
                    test_name = f"{model}-{parts[0]}-nt-{parts[1]}"
                    if test_name in all_scores:
                        has_nt_data = True
                        break
            if has_nt_data:
                model_configs.append((model, 'nt'))

        # Generate the data for each model
        for model_base, flag_variant in model_configs:

                display_name = f"{model_base} (nt)" if flag_variant == 'nt' else model_base
                f.write(f"| **{display_name}** |")

                max_score = -1
                scores_in_row = []

                # tr5 and tr6 use different patterns
                for config in configs:
                    # config example: 'tr5-05', 'tr6-10'
                    if flag_variant == 'nt':
                        # Insert nt- after tr5/tr6 in the config
                        # tr5-05 -> tr5-nt-05
                        parts = config.split('-')
                        if len(parts) == 2:  # tr5-05
                            test_name = f"{model_base}-{parts[0]}-nt-{parts[1]}"
                        else:
                            test_name = f"{model_base}-{config}"
                    else:
                        test_name = f"{model_base}-{config}"

                    score = all_scores.get(test_name)
                    scores_in_row.append(score)
                    if score is not None and score > max_score:
                        max_score = score

                # Output the scores
                for score in scores_in_row:
                    if score is None:
                        f.write(" - |")
                    elif score == max_score and max_score >= 0:
                        f.write(f" **{score}** |")
                    else:
                        f.write(f" {score} |")
                f.write("\n")

        f.write("\n")

        # Per-model practical-config list
        f.write("## Practical Settings List by Model\n\n")
        f.write(f"Accounting for score variation, the top 3 entries ({practical_threshold} or above) or the single highest-scoring entry for each model are set as a practical-level benchmark.\n\n")
        f.write("| Model | Score | Settings |\n")
        f.write("|:---|:---:|:---|\n")

        # Collect all scores
        # Track the base model name (for sorting) and the display model name (with flags) separately
        all_scores_by_model = {}  # {(base_model, display_model, score): [configs]}
        for test_name, score in all_scores.items():
            parsed = parse_test_name(test_name)
            if parsed:
                # Base model name (for sorting)
                base_model = parsed['model']
                # Display model name (with flags)
                display_model = get_model_display_name(parsed['model'], parsed['flags'])
                config = test_name.replace(f"{parsed['model']}-", "")
                key = (base_model, display_model, score)
                if key not in all_scores_by_model:
                    all_scores_by_model[key] = []
                all_scores_by_model[key].append(config)

        # Group by base model name -> (display model name, score, configs)
        models_scores = {}
        for (base_model, display_model, score), configs in all_scores_by_model.items():
            if base_model not in models_scores:
                models_scores[base_model] = []
            models_scores[base_model].append((display_model, score, configs))

        # Sort by descending score within each model and filter
        filtered_models_scores = {}
        for base_model, scores_list in models_scores.items():
            # Sort by descending score
            sorted_scores = sorted(scores_list, key=lambda x: -x[1])

            # Get the scores at or above practical_threshold
            scores_above_threshold = [s for s in sorted_scores if s[1] >= practical_threshold]

            # Filter
            if scores_above_threshold:
                # If there are scores at or above practical_threshold: up to the top 3 entries
                selected = scores_above_threshold[:3]
            else:
                # If there are none at or above the threshold: only the single highest-scoring entry
                selected = sorted_scores[:1]

            if selected:
                filtered_models_scores[base_model] = selected

        # Sort the models by descending highest score
        sorted_models = sorted(filtered_models_scores.keys(),
                              key=lambda m: -filtered_models_scores[m][0][1])

        # Output
        for base_model in sorted_models:
            for display_model, score, configs in filtered_models_scores[base_model]:
                # Join the configs with commas
                config_str = ', '.join(sorted(configs, key=natural_sort_key))
                f.write(f"| **{display_model}** | {score} | {config_str} |\n")

        # List of scores at or above highlight_threshold (filtered from the per-model practical-config list)
        f.write(f"\n### Scores of {highlight_threshold} and Above\n\n")
        f.write("| Model | Score | Settings |\n")
        f.write("|:---|:---:|:---|\n")

        # Output only scores >= 96, in the same order as the per-model practical-config list
        for base_model in sorted_models:
            for display_model, score, configs in filtered_models_scores[base_model]:
                if score >= highlight_threshold:
                    # Join the configs with commas
                    config_str = ', '.join(sorted(configs, key=natural_sort_key))
                    f.write(f"| **{display_model}** | {score} | {config_str} |\n")

def main():
    """Main processing"""
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Script to generate SCORES.md from SCORES.txt')
    parser.add_argument('scores_file', type=Path, help='Input file')
    parser.add_argument('-o', '--output', type=Path, help='Output file (default: change the input file extension to .md)')
    parser.add_argument('-1', '--practical-threshold', type=int, required=True,
                        help='Threshold score used to select the per-model practical-config list')
    parser.add_argument('-2', '--highlight-threshold', type=int, required=True,
                        help='Threshold score for the highlight score list')
    args = parser.parse_args()

    scores_file = args.scores_file
    output_file = args.output or scores_file.with_suffix('.md')

    if not scores_file.exists():
        print(f"Error: {scores_file} not found")
        return

    print(f"Reading SCORES.txt: {scores_file}")
    scores_by_model = parse_scores(scores_file)

    print(f"Generating Markdown file: {output_file}")
    generate_markdown(
        scores_by_model,
        output_file,
        practical_threshold=args.practical_threshold,
        highlight_threshold=args.highlight_threshold,
    )

    print(f"✓ Generated SCORES.md ({len(scores_by_model)} models)")

if __name__ == "__main__":
    main()
