from typing import Dict, List

from llm_service import generate_with_llm


REQUIRED_SECTIONS = [
    "PROJECT / TASK",
    "REQUIREMENTS",
    "DECISIONS",
    "CURRENT STATE",
    "ERRORS / ISSUES",
    "TODO / NEXT STEPS",
    "USER PREFERENCES",
    "CODE CONTEXT",
    "IMPORTANT CONTEXT",
]


def build_compression_input(messages: List[Dict]) -> Dict:
    conversation_parts = []

    for message in messages:
        role = str(message.get("role", "unknown")).upper()
        content = str(message.get("content", "")).strip()

        if not content:
            continue

        conversation_parts.append(
            f"[{role}]\n{content}"
        )

    conversation_text = "\n\n".join(conversation_parts)

    return {
        "message_count": len(conversation_parts),
        "conversation": conversation_text,
    }


def build_llm_text(compression_input: Dict) -> str:
    return compression_input.get("conversation", "").strip()


def build_compression_prompt(compression_input: Dict) -> str:
    conversation_text = build_llm_text(compression_input)

    return f"""
You are a context compression engine.

Your job is to create a compact but LOSSLESS continuation context
for another AI system.

The compressed context will be used by another AI to continue the
same task without access to the original conversation.

Do NOT invent information.
Do NOT remove important technical information just to make the
summary shorter.

You MUST return exactly these sections:

=== PROJECT / TASK ===
=== REQUIREMENTS ===
=== DECISIONS ===
=== CURRENT STATE ===
=== ERRORS / ISSUES ===
=== TODO / NEXT STEPS ===
=== USER PREFERENCES ===
=== CODE CONTEXT ===
=== IMPORTANT CONTEXT ===

CRITICAL PRESERVATION RULES:

1. Preserve the exact main project/task being discussed.

2. Preserve the core objective and what the user is trying to build,
solve, implement, debug, or achieve.

3. Preserve ALL explicit requirements and constraints.

4. Preserve important technical entities exactly when present,
including:
- programming languages
- frameworks
- libraries
- models
- algorithms
- datasets
- project names
- file paths
- filenames
- function names
- class names
- APIs
- tools

5. Preserve important relationships between concepts.

6. Preserve security, correctness and data-quality constraints.

7. Preserve decisions that affect future implementation.

8. Preserve unresolved errors and their causes when known.

9. Preserve TODOs and concrete next steps.

10. Preserve user preferences that affect how the task should continue.

11. Remove greetings, repetition, filler and irrelevant discussion.

12. Do not replace specific technical information with vague wording.

13. If information is present in the conversation, it MUST NOT be
omitted merely because it appears obvious.

14. NEVER omit any required section header.

15. You MUST output all 9 section headers exactly as specified,
even when a section has no information.

16. If a section has no information, write exactly:
None identified from the conversation.

17. The following headers are mandatory and must ALWAYS appear:

=== PROJECT / TASK ===
=== REQUIREMENTS ===
=== DECISIONS ===
=== CURRENT STATE ===
=== ERRORS / ISSUES ===
=== TODO / NEXT STEPS ===
=== USER PREFERENCES ===
=== CODE CONTEXT ===
=== IMPORTANT CONTEXT ===

=== CONVERSATION ===

{conversation_text}

=== END CONVERSATION ===

Now produce the compressed context using the exact section structure.
""".strip()


def ensure_required_sections(text: str) -> str:
    text = text.strip()

    missing_sections = []

    for section in REQUIRED_SECTIONS:
        header = f"=== {section} ==="

        if header not in text:
            missing_sections.append(section)

    for section in missing_sections:
        text += (
            f"\n\n=== {section} ===\n"
            "None identified from the conversation."
        )

    return text


def compress_with_llm(compression_input: Dict) -> str:
    prompt = build_compression_prompt(compression_input)

    try:
        raw_text = generate_with_llm(
            prompt,
            max_tokens=300,
        )
    except RuntimeError as exc:
        raise RuntimeError(
            f"LLM compression failed: {exc}"
        ) from exc

    return ensure_required_sections(raw_text)
