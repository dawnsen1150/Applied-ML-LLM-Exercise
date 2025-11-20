import json
import os
from typing import Literal, Optional

from openai import OpenAI
from pydantic import BaseModel


def get_openai_client(
    messages: list,
    response_format: BaseModel,
    type: Optional[Literal["openai", "ollama"]] = None,
):
    # Determine provider from env var or explicit parameter
    if type is None:
        model_type = os.getenv("MODEL_TYPE", "openai").lower()
        if model_type in ["openai", "ollama"]:
            type = model_type
        else:
            raise ValueError(
                f"Invalid MODEL_TYPE in environment: '{model_type}'. Must be 'openai' or 'ollama'"
            )

    if type == "openai":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.responses.parse(
            model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
            input=messages,
            text_format=response_format,
        )
        return response.output_parsed
    elif type == "ollama":
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
        # Ensure URL ends with /v1 for OpenAI-compatible endpoint
        if not ollama_url.endswith("/v1"):
            if ollama_url.endswith("/"):
                ollama_url = ollama_url + "v1"
            else:
                ollama_url = ollama_url + "/v1"

        client = OpenAI(
            base_url=ollama_url, api_key=os.getenv("OLLAMA_API_KEY", "ollama")
        )

        response = client.chat.completions.parse(
            model=os.getenv("MODEL_NAME", "gemma3:4b"),
            messages=messages,
            response_format=response_format,
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)
        structured_data = response_format(**data)
        return structured_data
    else:
        raise ValueError(f"Invalid type: {type}. Must be 'openai' or 'ollama'")
