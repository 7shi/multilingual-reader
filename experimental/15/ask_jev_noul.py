"""Ask Jev (one Noul per request) whether each text is written in the claimed language."""
from typesafe_sdk import Noul, TypeSafeClient

from ask_qwen_yesno import CASES  # same ten cases as the qwen3.6 run

MODEL = "jev-1.14.0"

QUESTION = Noul(
    instructions="Is `text` written in `claimed_language`?",
    criteria={
        "true": "The text is written in the claimed language.",
        "false": "The text is written in some other language.",
    },
)

with TypeSafeClient(timeout=120.0) as client:
    for lang, path, actual in CASES:
        text = open(path, encoding="utf-8").read().rstrip()
        state = {"claimed_language": lang, "text": text}
        response = client.system_one(state, {"is_claimed_language": QUESTION},
                                     model=MODEL)
        p = response.nouls["is_claimed_language"].noul
        print(f"claimed={lang:<10} actual={actual:<10} -> p(yes)={p:.4f}", flush=True)
