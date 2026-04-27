import json
import time
from typing import Type
from pydantic import BaseModel
from llm7shi.compat import generate_with_schema
from llm7shi import create_json_descriptions_prompt

DEFAULT_RETRY_WAIT_SECONDS = 3


class LLMClient:
    def __init__(self, model: str, max_length: int = 8192, think: bool = True,
                 retry_wait: int = DEFAULT_RETRY_WAIT_SECONDS, max_retries: int = 3):
        self.model = model
        self.max_length = max_length
        self.think = think
        self.retry_wait = retry_wait
        self.max_retries = max_retries

    def call(self, prompts: list, **kwargs) -> str:
        result = generate_with_schema(
            prompts,
            model=self.model,
            max_length=self.max_length,
            show_params=False,
            include_thoughts=self.think,
            **kwargs,
        )
        return result.text

    def call_json(self, prompts: list, schema: Type[BaseModel], **kwargs) -> dict:
        full_prompts = prompts + [create_json_descriptions_prompt(schema)]
        for attempt in range(self.max_retries):
            text = self.call(full_prompts, schema=schema, **kwargs)
            try:
                return json.loads(text)
            except json.JSONDecodeError as e:
                if attempt < self.max_retries - 1:
                    print(f"JSONデコードエラー（試行{attempt + 1}/{self.max_retries}）: {e}")
                    for i in range(self.retry_wait, -1, -1):
                        print(f"\rリトライ待ち... {i}s ", end="", flush=True)
                        time.sleep(1)
                    print()
                else:
                    print(f"JSONデコードに{self.max_retries}回失敗しました。")
                    raise
