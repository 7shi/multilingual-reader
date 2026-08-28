# Translation evaluation script (SCORE.md criteria)

import json
from pydantic import BaseModel, Field
from .llm import LLMClient, DEFAULT_RETRY_WAIT_SECONDS
from .statusline import StatusLine

class ReasoningAndScore(BaseModel):
    reasoning: str = Field(description="Detailed reasoning and consideration for scoring this evaluation criterion")
    score: int = Field(ge=0, le=20, description="Score out of 20 points")

class TranslationEvaluation(BaseModel):
    readability: ReasoningAndScore = Field(
        description="Readability and Comprehensibility (20 points): Evaluate whether target language readers can easily understand the content, whether complex concepts are explained clearly, and whether the sentence structure is logical and easy to follow"
    )
    fluency: ReasoningAndScore = Field(
        description="Fluency and Naturalness (20 points): Evaluate whether the translated text sounds natural and smooth to native speakers of the target language, whether there are unnatural expressions or awkward grammar, and whether vocabulary choices are appropriate and contemporary"
    )
    terminology: ReasoningAndScore = Field(
        description="Technical Terminology Appropriateness (20 points): Evaluate whether technical terms are appropriately handled according to the reader's understanding level, whether explanations or paraphrases are provided when necessary, and whether term selection is consistent"
    )
    contextual_adaptation: ReasoningAndScore = Field(
        description="Contextual Adaptation (20 points): Evaluate whether the original text's intent and purpose are effectively conveyed, whether expressions consider the target readers' cultural background, and whether expressions are improved or optimized as needed"
    )
    information_completeness: ReasoningAndScore = Field(
        description="Information Completeness (20 points): Evaluate whether important information from the original text is conveyed without omission, whether appropriate supplements are provided to aid reader understanding, and whether redundancy is eliminated while keeping the content concise and clear"
    )
    overall_comment: str = Field(
        description="Overall comprehensive evaluation comment about the translation quality as a whole"
    )

def add_parser(subparsers):
    parser = subparsers.add_parser("eval", help="Evaluate translation quality on 5 criteria")
    parser.add_argument("--original", required=True, help="Original text file")
    parser.add_argument("--translation", required=True, help="Translated text file")
    parser.add_argument("-m", "--model", required=True, help="Model used for evaluation")
    parser.add_argument("-f", "--from", dest="from_lang", required=True, help="Source language (e.g. English, Japanese)")
    parser.add_argument("-t", "--to", dest="to_lang", required=True, help="Target language (e.g. English, Japanese)")
    parser.add_argument("-o", "--output", dest="output_file", help="Filename to save the evaluation result as JSON")
    parser.add_argument("-w", "--retry-wait", type=int, default=DEFAULT_RETRY_WAIT_SECONDS,
                        help=f"Wait time on retry, in seconds (default: {DEFAULT_RETRY_WAIT_SECONDS}s)")
    parser.add_argument("--no-think", action="store_true", help="Disable thinking (for Qwen3 models)")
    parser.add_argument("--run", type=int, default=1, help="Current evaluation run number (default: 1)")
    parser.add_argument("--runs", type=int, default=1, help="Total number of evaluation runs (default: 1)")
    parser.set_defaults(func=run)
    return parser

def run(args):
    ui = StatusLine(
        label=getattr(args, 'label', None),
        start=getattr(args, 'start', None),
        index=getattr(args, 'index', None),
        count=getattr(args, 'count', None),
    )

    with open(args.original, "r", encoding="utf-8") as f:
        original_text = f.read().rstrip()

    with open(args.translation, "r", encoding="utf-8") as f:
        translated_text = f.read().rstrip()

    evaluation_prompt = f"""Please evaluate this translation from {args.from_lang} to {args.to_lang}.

**CRITICAL GUIDELINES**:
1. Verify translation exists and is in {args.to_lang}. If missing/incomplete, assign 0 points to ALL criteria.
2. Evaluate the ENTIRE file from beginning to end, not just the first or last lines.
3. Structural defects (mixed languages, JSON fragments, meta-commentary) are CRITICAL errors (0-5 points).
4. Major defects (grammatical errors, untranslated text) = 6-12 points.
5. Minor issues (awkward phrasing) = 13-17 points.
6. High quality (natural, accurate) = 18-20 points.

Score each criterion from 0-20 points based on the ENTIRE document."""

    schema = TranslationEvaluation
    prompts = [
        f"<original>\n{original_text}\n</original>",
        f"<translation>\n{translated_text}\n</translation>",
        evaluation_prompt,
    ]

    client = LLMClient(
        model=args.model,
        think=(not args.no_think),
        retry_wait=args.retry_wait,
    )

    run = getattr(args, 'run', 1)
    runs = getattr(args, 'runs', 1)
    with ui.progress(runs, start=run - 1) as prog:
        evaluation_result = client.call_json(prompts, schema=schema, file=ui.stream)
        ui.stream.end()
        prog.update(run)

    ui.write("=== Translation Evaluation Result ===\n")
    ui.write(f"1. Readability & comprehensibility: {evaluation_result['readability']['score']:2d}/20\n")
    ui.write(f"2. Fluency & naturalness           : {evaluation_result['fluency']['score']:2d}/20\n")
    ui.write(f"3. Terminology appropriateness     : {evaluation_result['terminology']['score']:2d}/20\n")
    ui.write(f"4. Contextual adaptation           : {evaluation_result['contextual_adaptation']['score']:2d}/20\n")
    ui.write(f"5. Information completeness        : {evaluation_result['information_completeness']['score']:2d}/20\n")

    total_score = (evaluation_result['readability']['score'] +
                   evaluation_result['fluency']['score'] +
                   evaluation_result['terminology']['score'] +
                   evaluation_result['contextual_adaptation']['score'] +
                   evaluation_result['information_completeness']['score'])
    ui.write(f"Total score: {total_score}/100\n")

    if args.output_file:
        output_data = {
            "original_file": args.original,
            "translation_file": args.translation,
            "source_language": args.from_lang,
            "target_language": args.to_lang,
            "model_used": args.model,
            "evaluation": evaluation_result,
            "total_score": total_score
        }
        with open(args.output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        ui.write(f"\nSaved evaluation result as JSON: {args.output_file}\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate translation quality on 5 criteria")
    subparsers = parser.add_subparsers()
    add_parser(subparsers)
    args = parser.parse_args(["eval"] + __import__("sys").argv[1:])
    args.func(args)
