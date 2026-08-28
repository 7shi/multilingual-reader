"""Static site builder for multilingual-reader.

Reads examples/{topic}-{lang}.txt and generates:
- dist/{topic}.html         multilingual parallel mode (default)
- dist/{topic}-{lang}.html  single-language mode (24 files)
- dist/index.html           landing page
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = ROOT / "examples"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = TEMPLATES_DIR / "static"
DIST_DIR = ROOT / "dist"

TOPIC_LABELS: dict[str, str] = {
    "transformer": "🤖 Transformer",
    "finetuning": "🎯 Fine-tuning",
    "onde": "🌊 Onde (Waves)",
    "momentum": "⚡ Momentum",
}

LANG_CONFIG: dict[str, dict] = {
    "fr": {"code": "fr-FR", "name": "Français", "default_rate": 1.0},
    "en": {"code": "en-US", "name": "English", "default_rate": 1.0},
    "es": {"code": "es-ES", "name": "Español", "default_rate": 1.0},
    "de": {"code": "de-DE", "name": "Deutsch", "default_rate": 1.0},
    "ja": {"code": "ja-JP", "name": "日本語", "default_rate": 1.4},
    "zh": {
        "code": "zh-CN",
        "name": "中文",
        "default_rate": 1.0,
        "font_family": [
            "Noto Sans SC",
            "Microsoft YaHei",
            "PingFang SC",
            "Hiragino Sans GB",
            "sans-serif",
        ],
    },
}


def normalize(text: str) -> str:
    """Replace control characters with spaces and collapse consecutive spaces into one."""
    normalized = "".join(" " if ord(ch) < 32 else ch for ch in text)
    normalized = re.sub(r" +", " ", normalized)
    return normalized.strip()


def extract_speaker_and_text(text: str) -> tuple[str | None, str]:
    """Extract (speaker, content) from a `speaker_name: utterance` format string.

    Supports both the Chinese fullwidth colon `：` (U+FF1A) and the ASCII colon `:`.
    """
    text = normalize(text)
    for sep in (":", "："):
        if sep in text:
            parts = text.split(sep, 1)
            if len(parts) == 2:
                return normalize(parts[0]), normalize(parts[1])
    return None, text


@dataclass
class Line:
    speaker: str
    text: str
    speaker_index: int


def parse_text_file(filepath: Path) -> tuple[list[Line], list[str]]:
    """Convert a text file into a list of Line, also returning speakers in order of appearance."""
    raw_lines = filepath.read_text(encoding="utf-8").splitlines()
    speakers_in_order: list[str] = []
    lines: list[Line] = []
    for raw in raw_lines:
        if not raw.strip():
            continue
        speaker, content = extract_speaker_and_text(raw)
        if speaker is None:
            continue
        if speaker not in speakers_in_order:
            speakers_in_order.append(speaker)
        speaker_index = speakers_in_order.index(speaker)
        lines.append(Line(speaker=speaker, text=content, speaker_index=speaker_index))
    return lines, speakers_in_order


def build_page(env: Environment, topic: str, lang: str) -> None:
    """Generate the HTML for a single topic × single language."""
    src = EXAMPLES_DIR / f"{topic}-{lang}.txt"
    if not src.exists():
        raise FileNotFoundError(src)

    lines, speakers = parse_text_file(src)
    cfg = LANG_CONFIG[lang]

    lang_nav = [
        {
            "code": "all",
            "label": "All",
            "name": "All languages",
            "href": f"{topic}.html",
            "current": False,
        }
    ]
    for code, lcfg in LANG_CONFIG.items():
        lang_nav.append({
            "code": code,
            "label": code.upper(),
            "name": lcfg["name"],
            "href": f"{topic}-{code}.html",
            "current": code == lang,
        })

    page_config = {
        "topic": topic,
        "lang": lang,
        "lang_code": cfg["code"],
        "lang_name": cfg["name"],
        "default_rate": cfg["default_rate"],
        "font_family": cfg.get("font_family"),
        "speakers": speakers,
    }

    config_json = json.dumps(page_config, ensure_ascii=False, indent=2)
    # Unicode-escape `<` `>` `&` so this can be embedded safely inside a script tag.
    config_json = config_json.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")

    template = env.get_template("page.html")
    html = template.render(
        topic=topic,
        topic_label=TOPIC_LABELS[topic],
        lang=lang,
        lang_code=cfg["code"],
        lang_name=cfg["name"],
        default_rate=cfg["default_rate"],
        lines=lines,
        lang_nav=lang_nav,
        page_config_json=config_json,
    )
    out = DIST_DIR / f"{topic}-{lang}.html"
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)} ({len(lines)} lines)")


def build_multi_page(env: Environment, topic: str) -> None:
    """Generate the multilingual parallel mode HTML for a single topic (dist/{topic}.html)."""
    # Load lines for all languages (fr's order of appearance is the basis for speaker_index)
    all_lines: dict[str, list[Line]] = {}
    for lang in LANG_CONFIG:
        src = EXAMPLES_DIR / f"{topic}-{lang}.txt"
        if not src.exists():
            raise FileNotFoundError(src)
        lines, _ = parse_text_file(src)
        all_lines[lang] = lines

    # Get speakers' order of appearance from the first language (fr); speaker_index is shared across all languages.
    base_lines = all_lines["fr"]
    speakers_in_order: list[str] = []
    for line in base_lines:
        if line.speaker not in speakers_in_order:
            speakers_in_order.append(line.speaker)

    # Expand into per-line × per-language entries (skip languages that have no line)
    max_lines = max(len(v) for v in all_lines.values())
    groups = []
    for i in range(max_lines):
        group = []
        speaker_index = 0
        if i < len(base_lines):
            speaker_index = speakers_in_order.index(base_lines[i].speaker)
        for code in LANG_CONFIG:
            lines = all_lines[code]
            if i < len(lines):
                group.append({
                    "lang": code,
                    "speaker": lines[i].speaker,
                    "text": lines[i].text,
                    "speaker_index": speaker_index,
                })
        groups.append(group)

    # Page config (language list, speakers' order of appearance)
    languages_cfg = []
    for code, cfg in LANG_CONFIG.items():
        item = {
            "code": code,
            "name": cfg["name"],
            "lang_code": cfg["code"],
            "default_rate": cfg["default_rate"],
        }
        if "font_family" in cfg:
            item["font_family"] = cfg["font_family"]
        languages_cfg.append(item)

    page_config = {
        "topic": topic,
        "languages": languages_cfg,
        "speakers": speakers_in_order,
    }

    lang_nav = [
        {
            "code": "all",
            "label": "All",
            "name": "All languages",
            "href": f"{topic}.html",
            "current": True,
        }
    ]
    for code, lcfg in LANG_CONFIG.items():
        lang_nav.append({
            "code": code,
            "label": code.upper(),
            "name": lcfg["name"],
            "href": f"{topic}-{code}.html",
            "current": False,
        })

    config_json = json.dumps(page_config, ensure_ascii=False, indent=2)
    config_json = config_json.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")

    template = env.get_template("multi.html")
    html = template.render(
        topic=topic,
        topic_label=TOPIC_LABELS[topic],
        groups=groups,
        lang_nav=lang_nav,
        page_config_json=config_json,
    )
    out = DIST_DIR / f"{topic}.html"
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)} (multi, {len(groups)} groups)")


def build_index(env: Environment) -> None:
    """Generate the 4x6 matrix landing page."""
    topics = [{"id": tid, "label": label} for tid, label in TOPIC_LABELS.items()]
    langs = [{"id": lid, "name": cfg["name"]} for lid, cfg in LANG_CONFIG.items()]
    template = env.get_template("index.html")
    html = template.render(topics=topics, langs=langs)
    out = DIST_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)}")


def copy_static() -> None:
    """Copy templates/static/* to dist/assets/."""
    assets = DIST_DIR / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    shutil.copytree(STATIC_DIR, assets)
    print(f"  copied static -> {assets.relative_to(ROOT)}")


def main() -> None:
    DIST_DIR.mkdir(exist_ok=True)
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html"]),
    )

    print("Building multi-language pages...")
    for topic in TOPIC_LABELS:
        build_multi_page(env, topic)

    print("Building single-language pages...")
    for topic in TOPIC_LABELS:
        for lang in LANG_CONFIG:
            build_page(env, topic, lang)

    print("Building index...")
    build_index(env)

    print("Copying static assets...")
    copy_static()

    print("Done.")


if __name__ == "__main__":
    main()
