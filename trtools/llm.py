from llm7shi.usage import find_usage_file

# Where usage is recorded, or None when it is not worth recording (local models).
# Set by init_usage_path(); shared so that a caller running several subcommands
# (e.g. batch) can print the day's totals once at the end.
USAGE_PATH = None


def init_usage_path(model: str, save_usage: bool = False):
    """Set USAGE_PATH if usage should be recorded for this model, and return it."""
    global USAGE_PATH
    if model.startswith(("openai:", "gpt-")) or save_usage:
        USAGE_PATH = find_usage_file()
    return USAGE_PATH
