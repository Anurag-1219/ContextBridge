from typing import List, Dict
import ollama


def build_compression_input(messages: List[Dict]) -> Dict:
    context = {
        "requirements": [],
        "decisions": [],
        "errors": [],
        "todos": [],
        "preferences": [],
        "code": []
    }

    important_messages = []

    for message in messages:
        score = message.get("importance_score", 0.0)

        if score >= 0.40:
            important_messages.append({
                "message_id": message["message_id"],
                "role": message["role"],
                "content": message["content"],
                "importance_score": score
            })

        categories = message.get("categories", [])

        if "requirement" in categories:
            context["requirements"].append(message["content"])

        if "decision" in categories:
            context["decisions"].append(message["content"])

        if "error" in categories:
            context["errors"].append({
                "content": message["content"],
                "error_details": message.get(
                    "code_analysis", {}
                ).get("errors", [])
            })

        if "todo" in categories:
            context["todos"].append(message["content"])

        if "preference" in categories:
            context["preferences"].append(message["content"])

        code_analysis = message.get("code_analysis", {})

        if code_analysis.get("is_code"):
            context["code"].append({
                "message_id": message["message_id"],
                "language": code_analysis.get("language", "unknown"),
                "code_blocks": code_analysis.get("code_blocks", []),
                "file_paths": code_analysis.get("file_paths", []),
                "functions": code_analysis.get("functions", []),
                "classes": code_analysis.get("classes", []),
                "errors": code_analysis.get("errors", [])
            })

    return {
        "important_messages": important_messages,
        "context": context
    }


def build_llm_text(compression_input: Dict) -> str:
    context = compression_input["context"]
    sections = []

    sections.append("=== REQUIREMENTS ===")
    sections.extend(f"- {item}" for item in context["requirements"])

    sections.append("\n=== DECISIONS ===")
    sections.extend(f"- {item}" for item in context["decisions"])

    sections.append("\n=== ERRORS ===")

    for error in context["errors"]:
        sections.append(f"- {error['content']}")

        if error["error_details"]:
            sections.append(
                f"  Error details: {', '.join(error['error_details'])}"
            )

    sections.append("\n=== TODOS ===")
    sections.extend(f"- {item}" for item in context["todos"])

    sections.append("\n=== PREFERENCES ===")
    sections.extend(f"- {item}" for item in context["preferences"])

    sections.append("\n=== CODE ===")

    for code_item in context["code"]:
        sections.append(f"Language: {code_item['language']}")

        if code_item["file_paths"]:
            sections.append(
                "Files: " + ", ".join(code_item["file_paths"])
            )

        if code_item["functions"]:
            sections.append(
                "Functions: " + ", ".join(code_item["functions"])
            )

        if code_item["classes"]:
            sections.append(
                "Classes: " + ", ".join(code_item["classes"])
            )

        for block in code_item["code_blocks"]:
            sections.append(f"\n```{block['language']}")
            sections.append(block["content"])
            sections.append("```")

    sections.append("\n=== IMPORTANT MESSAGES ===")

    for message in compression_input["important_messages"]:
        sections.append(
            f"[{message['role'].upper()} | "
            f"importance={message['importance_score']}]"
        )
        sections.append(message["content"])

    return "\n".join(sections)


def build_compression_prompt(compression_input: Dict) -> str:
    llm_text = build_llm_text(compression_input)

    prompt = f"""
You are a context compression engine.

Compress the conversation context so another AI can continue the task.

RULES:

1. Preserve important requirements.
2. Preserve important decisions.
3. Preserve unresolved errors.
4. Preserve TODOs and unfinished work.
5. Preserve user preferences.
6. Preserve important code and technical details.
7. Preserve project/task state.
8. Remove greetings, repetition and irrelevant information.
9. Do not invent facts.
10. Do not change the meaning.
11. Keep information required for future debugging.
12. Make the result significantly shorter than the original.

Return exactly these sections:

=== PROJECT / TASK ===

=== REQUIREMENTS ===

=== DECISIONS ===

=== CURRENT STATE ===

=== ERRORS / ISSUES ===

=== TODO / NEXT STEPS ===

=== USER PREFERENCES ===

=== CODE CONTEXT ===

=== IMPORTANT CONTEXT ===

=== ORIGINAL CONTEXT ===
{llm_text}
"""

    return prompt.strip()


def compress_with_llm(compression_input: Dict) -> str:
    prompt = build_compression_prompt(compression_input)

    response = ollama.chat(
        model="qwen3.5:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=False,
        options={
            "num_ctx": 2048,
            "num_predict": 300
        }
    )

    content = response["message"]["content"]

    if not content or not content.strip():
        raise RuntimeError("LLM returned an empty compression response.")

    return content.strip()
