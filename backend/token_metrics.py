from typing import Dict


def estimate_text_tokens(text: str) -> int:
    """
    Rough token estimation.
    Approximation: 1 token ≈ 4 characters.
    """

    if not text:
        return 0

    return max(1, len(text) // 4)


def calculate_token_reduction(
    original_text: str,
    compressed_text: str
) -> Dict:

    original_tokens = estimate_text_tokens(original_text)
    compressed_tokens = estimate_text_tokens(compressed_text)

    tokens_saved = original_tokens - compressed_tokens

    if original_tokens == 0:
        reduction_percent = 0.0
    else:
        reduction_percent = (
            (original_tokens - compressed_tokens)
            / original_tokens
        ) * 100

    return {
        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,
        "tokens_saved": tokens_saved,
        "reduction_percent": round(reduction_percent, 2),
        "compression_effective": compressed_tokens < original_tokens
    }
