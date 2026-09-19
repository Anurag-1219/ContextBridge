from typing import List, Dict
import ollama

from compression import build_compression_input, build_compression_prompt


MODEL_NAME = "qwen3.5:4b"


def compress_conversation(messages: List[Dict]) -> Dict:
    compression_input = build_compression_input(messages)

    prompt = build_compression_prompt(compression_input)

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    compressed_context = response["message"]["content"].strip()

    return {
        "success": True,
        "model": MODEL_NAME,
        "compressed_context": compressed_context,
        "input_messages": len(messages)
    }
