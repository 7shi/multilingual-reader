import argparse
import time
from tqdm import tqdm
from trtools.llm import LLMClient

parser = argparse.ArgumentParser(description="Translation revision script using third-party evaluation (single-step CoT)")
parser.add_argument("--original", required=True, help="Original text file")
parser.add_argument("--translation", required=True, help="Baseline translation text file")
parser.add_argument("-f", "--from", dest="from_lang", required=True, help="Source language (e.g. English)")
parser.add_argument("-t", "--to", dest="to_lang", required=True, help="Target language (e.g. Dutch)")
parser.add_argument("-o", "--output", required=True, help="Output file name for the revised text")
parser.add_argument("-m", "--model", required=True, help="Model to use for revision")
parser.add_argument("--history", type=int, default=10, help="Number of context history entries")
parser.add_argument("--no-think", action="store_true", help="Disable CoT")
args = parser.parse_args()

with open(args.original, "r", encoding="utf-8") as f:
    orig_lines = f.readlines()
with open(args.translation, "r", encoding="utf-8") as f:
    tr_lines = f.readlines()

if len(orig_lines) != len(tr_lines):
    print("Warning: The number of lines in original and translation files do not match.")

client = LLMClient(model=args.model, think=not args.no_think)

context_history = []
results = []

for i, (orig_line, tr_line) in enumerate(zip(orig_lines, tr_lines)):
    orig_line = orig_line.strip()
    tr_line = tr_line.strip()
    
    if not orig_line or ":" not in orig_line:
        results.append(tr_line)
        continue
    
    print(f"\n[{i+1}/{len(orig_lines)}]")
    print(f"Original: {orig_line}")
    print(f"Base: {tr_line}")
    
    speaker, text = orig_line.split(":", 1)
    speaker = speaker.strip()
    text = text.strip()
    
    if ":" in tr_line:
        tr_speaker, tr_text = tr_line.split(":", 1)
        tr_speaker = tr_speaker.strip()
        tr_text = tr_text.strip()
    else:
        tr_speaker = speaker
        tr_text = tr_line

    chat_history = []
    
    system_msg = {
        "role": "system",
        "content": f"You are an expert {args.to_lang} reviewer. Your task is to review and refine a {args.from_lang} to {args.to_lang} translation."
    }
    chat_history.append(system_msg)
    
    if context_history and args.history > 0:
        context_prompt = "Previous context:\n\n"
        for ctx in context_history[-args.history:]:
            context_prompt += f"Original: {ctx['original']}\nTranslation: {ctx['translation']}\n\n"
        chat_history.append({"role": "user", "content": context_prompt.strip()})
        chat_history.append({"role": "assistant", "content": "Understood. I will use this context for consistency."})

    # Single-step prompt
    prompt = f"""Original {args.from_lang} text:
{text}

Base {args.to_lang} translation:
{tr_text}

Analyze this translation internally for literal translations, interference from other languages, unnatural phrasing, or grammar issues.
Then output ONLY the final improved {args.to_lang} translation text — nothing else. No analysis, no labels, no speaker name '{speaker}:', no quotes, no explanations. If the base translation is already perfect, output it exactly as-is."""

    chat_history.append({"role": "user", "content": prompt})
    
    print("\nRefined:")
    # The llm7shi client streams output in real time and uses CoT (think=True)
    improved_tr = client.call(chat_history)
    improved_tr = improved_tr.strip()
    
    # clean up quotes if the model wrapped it
    if improved_tr.startswith('"') and improved_tr.endswith('"'):
        improved_tr = improved_tr[1:-1].strip()
    
    # Sometimes the model might append extra blank lines or notes despite instructions
    # If the output contains <think>, it's usually stripped by llm7shi if include_thoughts handles it properly.
    # Otherwise we just use the raw output.
    
    # Let's save the original and translation to context
    results.append(f"{speaker}: {improved_tr}")
    
    context_history.append({
        'original': orig_line,
        'translation': f"{speaker}: {improved_tr}"
    })

with open(args.output, "w", encoding="utf-8") as f:
    for line in results:
        f.write(line + "\n")
        
print(f"\nReview complete. Saved to {args.output}")
