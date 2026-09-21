from typing import Dict


HANDOFF_SECTIONS = [
    "PROJECT / TASK",
    "REQUIREMENTS",
    "DECISIONS",
    "CURRENT STATE",
    "ERRORS / ISSUES",
    "TODO / NEXT STEPS",
    "USER PREFERENCES",
    "CODE CONTEXT",
    "IMPORTANT CONTEXT"
]


def build_handoff(sections: Dict) -> Dict:
    handoff = {
        "project_task": sections.get("PROJECT / TASK", ""),
        "requirements": sections.get("REQUIREMENTS", ""),
        "decisions": sections.get("DECISIONS", ""),
        "current_state": sections.get("CURRENT STATE", ""),
        "errors": sections.get("ERRORS / ISSUES", ""),
        "todos": sections.get("TODO / NEXT STEPS", ""),
        "user_preferences": sections.get("USER PREFERENCES", ""),
        "code_context": sections.get("CODE CONTEXT", ""),
        "important_context": sections.get("IMPORTANT CONTEXT", "")
    }

    return handoff


def validate_handoff(handoff: Dict) -> Dict:
    required_fields = [
        "project_task",
        "requirements",
        "decisions",
        "current_state",
        "errors",
        "todos",
        "user_preferences",
        "code_context",
        "important_context"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in handoff
    ]

    empty_fields = [
        field
        for field in required_fields
        if field in handoff
        and not str(handoff[field]).strip()
    ]

    return {
        "valid": len(missing_fields) == 0,
        "missing_fields": missing_fields,
        "empty_fields": empty_fields,
        "field_count": len(handoff)
    }


def build_handoff_prompt(handoff: Dict) -> str:
    prompt = f"""
You are continuing a task from a previous AI conversation.

Use the context below as the source of truth for the previous conversation.

Do not invent missing information.
Do not repeat the entire context unnecessarily.
Continue the task from the current state.
If information is missing, ask the user for it.

=== PROJECT / TASK ===
{handoff.get("project_task", "")}

=== REQUIREMENTS ===
{handoff.get("requirements", "")}

=== DECISIONS ===
{handoff.get("decisions", "")}

=== CURRENT STATE ===
{handoff.get("current_state", "")}

=== ERRORS / ISSUES ===
{handoff.get("errors", "")}

=== TODO / NEXT STEPS ===
{handoff.get("todos", "")}

=== USER PREFERENCES ===
{handoff.get("user_preferences", "")}

=== CODE CONTEXT ===
{handoff.get("code_context", "")}

=== IMPORTANT CONTEXT ===
{handoff.get("important_context", "")}

Now continue the task from the current state.
""".strip()

    return prompt
