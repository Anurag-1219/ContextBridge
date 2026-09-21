import json
from pathlib import Path
from typing import Dict


def load_handoff_json(
    input_path: str = "contextbridge_handoff.json"
) -> Dict:

    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Handoff file not found: {input_path}"
        )

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        package = json.load(file)

    return package


def validate_loaded_handoff(package: Dict) -> Dict:

    required_metadata = [
        "handoff_id",
        "created_at",
        "version",
        "source"
    ]

    required_context = [
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

    metadata = package.get("metadata", {})
    context = package.get("context", {})

    missing_metadata = [
        field
        for field in required_metadata
        if field not in metadata
    ]

    missing_context = [
        field
        for field in required_context
        if field not in context
    ]

    return {
        "valid": (
            len(missing_metadata) == 0
            and len(missing_context) == 0
        ),
        "missing_metadata": missing_metadata,
        "missing_context": missing_context
    }
