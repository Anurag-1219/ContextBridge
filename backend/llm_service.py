import os

import ollama
from openai import OpenAI


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")


def generate_with_llm(prompt: str, max_tokens: int = 300) -> str:

    if LLM_PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
            max_output_tokens=max_tokens,
        )

        return response.output_text.strip()

    if LLM_PROVIDER == "ollama":
        try:
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                think=False,
                options={
                    "num_ctx": 2048,
                    "num_predict": max_tokens,
                    "temperature": 0,
                },
            )
        except Exception as exc:
            raise RuntimeError(
                f"Ollama request failed: {exc}"
            ) from exc

        return response["message"]["content"].strip()

    raise RuntimeError(
        f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}"
    )
