import json
import sys
from typing import Type
from pydantic import BaseModel
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt, wait_retry, error
from llm7shi.usage import Usage, find_usage_file

DEFAULT_RETRY_WAIT_SECONDS = 3

# Where usage is recorded, or None when it is not worth recording (local models).
# Set by init_usage_path(); shared so that a caller running several subcommands
# (e.g. batch) can print the day's totals once at the end.
USAGE_PATH = None


def init_usage_path(model: str, save_usage: bool = False):
    """Set USAGE_PATH if usage should be recorded for this model, and return it."""
    global USAGE_PATH
    if model.startswith("openai:") or model.startswith("gpt-") or save_usage:
        USAGE_PATH = find_usage_file()
    return USAGE_PATH


class LLMClient:
    def __init__(self, model: str, max_length: int = 8192, think: bool = True,
                 retry_wait: int = DEFAULT_RETRY_WAIT_SECONDS, max_retries: int = 3):
        self.model = model
        self.max_length = max_length
        self.think = think
        self.retry_wait = retry_wait
        self.max_retries = max_retries
        # Usage summed over every call made through this client
        self.usage = Usage()

    def call(self, prompts: list, **kwargs) -> str:
        result = generate_with_schema(
            prompts,
            model=self.model,
            max_length=self.max_length,
            show_params=False,
            include_thoughts=self.think,
            **kwargs,
        )
        if result.usage:
            self.usage = self.usage + result.usage
        return result.text

    def call_json(self, prompts: list, schema: Type[BaseModel], **kwargs) -> dict:
        full_prompts = prompts + [create_json_descriptions_prompt(schema)]
        file = kwargs.get("file", sys.stderr)
        for attempt in range(self.max_retries):
            text = self.call(full_prompts, schema=schema, **kwargs)
            try:
                return json.loads(text)
            except json.JSONDecodeError as e:
                if attempt < self.max_retries - 1:
                    error(f"JSON decode error (attempt {attempt + 1}/{self.max_retries}): {e}", file=file)
                    wait_retry(self.retry_wait, "Waiting to retry...", file=file)
                else:
                    error(f"JSON decoding failed {self.max_retries} times.", file=file)
                    raise
