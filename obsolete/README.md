# Obsolete

Stores scripts whose specs are outdated.

## translate.py / translate.md

Old translation script replaced by the `trtools translate` subcommand. It implemented speaker separation, reasoning-level-based structured output, and sliding-window history management, but was retired for the following reasons:

- Raising the reasoning level did not improve translation quality (per experimental results)
- Sliding-window history management caused terminology drift and disabled the KV cache
- Speaker separation hurt generality

`translate.md` is a development log (the history of trying multi-stage translation and multi-model collaboration).

See `trtools/translate.py` (`uv run trtools translate`) for the new implementation.

## convert_genspark.py

Script that extracts per-speaker dialogue data from Genspark HTML files.

### Usage (at the time)

```bash
# Basic usage (default speaker names A,B)
uv run convert_genspark.py input.html -o output.txt

# Specify speaker names
uv run convert_genspark.py input.html -o output.txt --speaker Camille,Luc
```

### Features

- Extracts per-speaker dialogue data from Genspark HTML files
- Speaker names can be specified as a comma-separated list via `--speaker`
- Defaults to speaker names A,B
- Efficient HTML parsing via a pull-style XML parser
- Multilingual support via UTF-8 encoding

### Steps for adding a new dataset (at the time)

When generated with Genspark:

1. Copy the relevant DOM section from Genspark's output and save it as an HTML file
2. Extract the dialogue data using `convert_genspark.py`:

```bash
uv run convert_genspark.py genspark_output.html -o base_dialogue.txt --speaker Camille,Luc
```

### Input sample: genspark/

`obsolete/genspark/` holds 3 snapshot files of Genspark output from that time (transformer.html / onde.html / momentum.html). These are the original data behind the French source text that seeded the current `examples/{topic}-{lang}.txt` series, saved by copying Genspark's DOM. They can be referenced as sample input formats for convert_genspark.py.
