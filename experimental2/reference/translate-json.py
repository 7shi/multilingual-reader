import json
import argparse
from llm7shi.ollama import generate_content

# Parse command line arguments
parser = argparse.ArgumentParser(description='Translate transcriptions using LLM with history management')
parser.add_argument('input_file', type=str,
                    help='Input JSON file to translate')
parser.add_argument('-o', '--output', type=str, required=True,
                    help='Output JSON file for translations (required)')
parser.add_argument('-s', '--source-lang', type=str, required=True,
                    help='Source language (required)')
parser.add_argument('-t', '--target-lang', type=str, required=True,
                    help='Target language (required)')
parser.add_argument('-m', '--model', type=str, default='gpt-oss:120b',
                    help='Model to use for translation (default: gpt-oss:120b)')
parser.add_argument('--threshold', type=int, default=15,
                    help='Number of message pairs before compression (default: 15)')
parser.add_argument('--keep', type=int, default=5,
                    help='Number of recent message pairs to keep after compression (default: 5)')
parser.add_argument('--summary', type=str, default=None, choices=['patterns', 'summary'],
                    help='Summary generation method: "patterns" extracts translation patterns, "summary" creates English summary. If not specified, no summary is generated (fastest)')
parser.add_argument('--no-think', action='store_true',
                    help='Disable thinking mode (passes think=False to generate_content)')
args = parser.parse_args()

INPUT_FILE = args.input_file
OUTPUT_FILE = args.output
SOURCE_LANG = args.source_lang
TARGET_LANG = args.target_lang
MODEL = args.model
THRESHOLD = args.threshold
KEEP = args.keep
SUMMARY_TYPE = args.summary
THINK = not args.no_think

# Load the JSON file
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# System prompt (kept separate from message history)
system_message = {
    'role': 'system',
    'content': f'You are a professional translator. Translate the following {SOURCE_LANG} text to {TARGET_LANG}. Maintain consistency with previous translations and preserve the context and nuance of the original text. Provide only the translation without any explanations or commentary.',
}


def call_llm(prompt):
    """
    Call LLM and automatically add prompt and response to chat_history.

    Args:
        prompt: User prompt text

    Returns:
        Tuple of (response_text, user_message, assistant_message)
    """
    user_message = {'role': 'user', 'content': prompt}
    chat_history.append(user_message)

    response = generate_content(chat_history, model=MODEL, think=THINK)
    response_text = response.text.strip()

    assistant_message = {'role': 'assistant', 'content': response_text}
    chat_history.append(assistant_message)

    return response_text, user_message, assistant_message


def summarize_messages(summary_type):
    """
    Summarize translation history to extract patterns and important information.
    Automatically adds the summary request and response to chat_history.

    Args:
        summary_type: Type of summary ('patterns' or 'summary')

    Returns:
        Tuple of (summary_text, user_message, assistant_message)
    """
    # Create compression request based on summary type
    if summary_type == 'patterns':
        summary_content = (
            "Please compress the above translation history into a concise summary. "
            "Extract the following information:\n"
            "- Proper nouns and their translations (names, places, titles, etc.)\n"
            "- Important terminology and their translations\n"
            "- Speaking style and tone patterns for each speaker\n"
            "- Expressions and styles that should be kept consistent\n\n"
            "Provide a concise bullet-point summary that will help maintain consistency in future translations."
        )
    else:  # summary_type == 'summary'
        summary_content = (
            "Please create a concise English summary of the translation pairs above. "
            "Focus on the content and context of what was discussed or described. "
            "Do NOT extract translation patterns, speaking styles, or terminology. "
            "If there is an existing summary, integrate the new content with it."
        )

    # Call LLM and automatically update chat_history
    summary_text, user_message, assistant_message = call_llm(summary_content)

    return summary_text, user_message, assistant_message


# Initialize message history
translation_messages = []  # Cumulative translation (U, A) pairs
summary_messages = []      # Cumulative summary (U, A) pairs
chat_history = [system_message]  # Complete chat history for LLM
next_compression = None  # Track next compression timing

# Create a new structure to store translations
translated_data = {
    'transcriptions': []
}

print(f"Translating {len(data['transcriptions'])} entries...")

# Translate each transcription
for i, entry in enumerate(data['transcriptions'], 1):
    time = entry['time']
    speaker = entry['speaker']
    original_text = entry['transcription']

    print()
    print(f"[{i}/{len(data['transcriptions'])}] {time} - {speaker}")
    print(f"Original: {original_text}")

    # Get translation from LLM
    translated_text, user_message, assistant_message = call_llm(
        f'Translate to {TARGET_LANG}: {original_text}'
    )

    # Add to translation messages
    translation_messages.append(user_message)
    translation_messages.append(assistant_message)

    #print(f"Translation: {translated_text}")

    # Update next_compression timing (after translation 10, 20, 30...)
    if i % (THRESHOLD - KEEP) == 0:
        next_compression = i + KEEP if i + KEEP <= len(data['transcriptions']) else None

        # Generate summary only if SUMMARY_TYPE is specified and we'll reach next compression
        if SUMMARY_TYPE is not None and next_compression is not None:
            print()
            print(f"[Generating summary after translation {i} (cache-efficient timing)]")

            summary_text, summary_request, summary_response = summarize_messages(SUMMARY_TYPE)

            # Add to summary_messages
            summary_messages.append(summary_request)
            summary_messages.append(summary_response)

            print(f"[Summary generated and added to history]")
            #print(f"[Summary content]\n{summary_text}\n")

    # Check if compression is needed (at next_compression timing)
    if next_compression is not None and i == next_compression:
        print()
        print(f"[Compressing history after translation {i}: keeping {KEEP} pairs]")

        # Rebuild chat_history
        if SUMMARY_TYPE is None:
            # No summary mode: only keep recent translations
            chat_history = [system_message] + translation_messages[-KEEP*2:]
        else:
            # Summary mode: keep latest summary + recent translations
            chat_history = [system_message] + summary_messages[-2:] + translation_messages[-KEEP*2:]

        print(f"[Compression complete. Context: {('summary + ' if SUMMARY_TYPE else '')}{KEEP} pairs]")

    # Add to translated data
    translated_data['transcriptions'].append({
        'time': time,
        'speaker': speaker,
        'original': original_text,
        'translation': translated_text
    })

# Save the translated JSON
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(translated_data, f, ensure_ascii=False, indent=2)

print(f"Translation complete! Saved to {OUTPUT_FILE}")
