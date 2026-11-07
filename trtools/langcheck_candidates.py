"""Languages `trtools langcheck` offers Jev beside the target, per target code.

Copied from experimental/15/results/candidates-gpt-6-sol.json, which is rebuilt by
experimental/15/calibrate_jev.py: the languages that drew 0.01 or more, either way, when
Jev picked each text's language from all languages + English + Other. A target missing
here has nothing it was confused with and is offered alone; the source language and
`Other` are added at run time.

Part of the check scheme: LANGCHECK_ID in langcheck.py hashes this table.
"""

CANDIDATES = {
    "da": ["Norwegian"],
    "eo": ["Interlingua"],
    "es": ["French"],
    "fa": ["Urdu"],
    "fr": ["Spanish"],
    "hr": ["Serbian", "Slovene"],
    "ia": ["Esperanto", "Italian"],
    "id": ["Malay"],
    "it": ["Interlingua"],
    "kn": ["Telugu"],
    "lo": ["Thai"],
    "lv": ["Slovene"],
    "ms": ["Indonesian"],
    "no": ["Danish"],
    "sl": ["Croatian", "Latvian"],
    "sr": ["Croatian"],
    "te": ["Kannada"],
    "th": ["Lao"],
    "ur": ["Persian"],
}
