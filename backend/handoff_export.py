import json
from pathlib import Path
from typing import Dict


def export_handoff_json(
    package: Dict,
    output_path: str = "contextbridge_handoff.json"
) -> str:

    path = Path(output_path)

    with path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            package,
            file,
            indent=2,
            ensure_ascii=False
        )

    return str(path)
