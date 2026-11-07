"""Ask Jev (one Choice per request) whether each text is in English or the claimed language."""
from typesafe_sdk import Choice, TypeSafeClient

from ask_qwen_yesno import CASES  # same ten cases as the qwen3.6 and Noul runs

MODEL = "jev-1.14.0"


def question(lang):
    return Choice(
        instructions="Which language is `text` written in?",
        criteria={
            "English": "The text is written in English.",
            lang: f"The text is written in {lang}.",
        },
    )


with TypeSafeClient(timeout=120.0) as client:
    for lang, path, actual in CASES:
        text = open(path, encoding="utf-8").read().rstrip()
        response = client.system_one({"text": text}, {"language": question(lang)},
                                     model=MODEL)
        a = response.choices["language"]
        probs = " ".join(f"{k}={v:.4f}" for k, v in a.probabilities.items())
        print(f"claimed={lang:<10} actual={actual:<10} -> {a.choice:<10} {probs}",
              flush=True)
