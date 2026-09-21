from typing import Dict, List


REQUIRED_SECTIONS = [
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


def build_compression_schema(
    compressed_text: str
) -> Dict:

    if not compressed_text:
        return {
            "success": False,
            "error": "Empty compression output.",
            "sections": {}
        }

    text = compressed_text.strip()

    sections = {}

    positions = []

    for section in REQUIRED_SECTIONS:

        marker = f"=== {section} ==="

        position = text.find(marker)

        if position == -1:
            return {
                "success": False,
                "error": f"Missing section: {section}",
                "sections": sections
            }

        positions.append(
            (position, section, marker)
        )


    positions.sort(
        key=lambda item: item[0]
    )


    for index, (
        position,
        section,
        marker
    ) in enumerate(positions):

        content_start = (
            position + len(marker)
        )

        if index + 1 < len(positions):

            next_position = positions[
                index + 1
            ][0]

            content = text[
                content_start:next_position
            ].strip()

        else:

            content = text[
                content_start:
            ].strip()


        sections[section] = content


    return {
        "success": True,
        "sections": sections,
        "section_count": len(sections)
    }
