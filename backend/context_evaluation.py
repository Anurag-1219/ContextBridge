from typing import Dict, List, Set
import re


STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were",
    "be", "to", "of", "on", "in", "for", "and",
    "or", "only", "must", "should", "use", "using",
    "build", "built", "implementation", "implement",
    "system", "develop", "development"
}


def normalize_for_comparison(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_keywords(text: str) -> Set[str]:
    normalized = normalize_for_comparison(text)

    words = normalized.split()

    return {
        word
        for word in words
        if word not in STOP_WORDS
        and len(word) > 2
    }


def check_context_preservation(
    original_items: List[str],
    compressed_text: str,
    threshold: float = 0.50
) -> Dict:

    compressed_keywords = extract_keywords(
        compressed_text
    )

    results = []

    for item in original_items:

        original_keywords = extract_keywords(item)

        if not original_keywords:
            continue

        matched_keywords = (
            original_keywords
            & compressed_keywords
        )

        overlap = (
            len(matched_keywords)
            / len(original_keywords)
        )

        preserved = overlap >= threshold

        results.append({
            "item": item,
            "preserved": preserved,
            "overlap": round(overlap, 2),
            "matched_keywords": sorted(
                matched_keywords
            )
        })

    preserved_count = sum(
        1
        for result in results
        if result["preserved"]
    )

    total_items = len(results)

    preservation_rate = (
        preserved_count / total_items * 100
        if total_items
        else 0.0
    )

    return {
        "total_items": total_items,
        "preserved_items": preserved_count,
        "lost_items": total_items - preserved_count,
        "preservation_rate": round(
            preservation_rate,
            2
        ),
        "results": results
    }


def evaluate_requirements(
    original_requirements: List[str],
    compressed_text: str,
    threshold: float = 0.50
) -> Dict:

    compressed_keywords = extract_keywords(compressed_text)
    normalized_compressed = normalize_for_comparison(compressed_text)

    semantic_groups = {
        "fraud": {"fraud"},
        "detection": {"detection", "detect"},
        "python": {"python"},
        "avoid": {"avoid", "prevent", "prevention"},
        "data": {"data"},
        "leakage": {"leakage", "leak", "contamination"},
        "chronological": {"chronological", "temporal", "time"},
        "split": {"split", "splitting"},
        "preprocessing": {"preprocessing", "preprocess"},
        "fit": {"fit", "fitted", "fitting"},
        "training": {"training", "train"},
        "test": {"test", "testing"}
    }

    results = []

    for requirement in original_requirements:

        requirement_keywords = extract_keywords(requirement)

        if not requirement_keywords:
            continue

        matched_keywords = (
            requirement_keywords
            & compressed_keywords
        )

        overlap = (
            len(matched_keywords)
            / len(requirement_keywords)
        )

        normalized_requirement = normalize_for_comparison(
            requirement
        )

        words = normalized_requirement.split()

        important_phrases = []

        for i in range(len(words) - 1):

            first = words[i]
            second = words[i + 1]

            if len(first) >= 4 and len(second) >= 4:
                important_phrases.append(
                    f"{first} {second}"
                )

        matched_phrases = [
            phrase
            for phrase in important_phrases
            if phrase in normalized_compressed
        ]

        phrase_score = (
            len(matched_phrases)
            / len(important_phrases)
            if important_phrases
            else 0.0
        )

        semantic_matches = set()

        for keyword in requirement_keywords:

            if keyword in compressed_keywords:
                semantic_matches.add(keyword)
                continue

            for group in semantic_groups.values():

                if keyword in group and (
                    group & compressed_keywords
                ):
                    semantic_matches.add(keyword)
                    break

        semantic_overlap = (
            len(semantic_matches)
            / len(requirement_keywords)
            if requirement_keywords
            else 0.0
        )

        preserved = (
            overlap >= threshold
            or phrase_score >= 0.40
            or semantic_overlap >= threshold
        )

        results.append({
            "requirement": requirement,
            "preserved": preserved,
            "overlap": round(overlap, 2),
            "phrase_score": round(phrase_score, 2),
            "semantic_overlap": round(
                semantic_overlap, 2
            ),
            "matched_keywords": sorted(
                matched_keywords
            ),
            "matched_phrases": sorted(
                matched_phrases
            ),
            "semantic_matches": sorted(
                semantic_matches
            )
        })

    total_requirements = len(results)

    preserved_requirements = sum(
        1
        for result in results
        if result["preserved"]
    )

    lost_requirements = (
        total_requirements
        - preserved_requirements
    )

    preservation_rate = (
        preserved_requirements
        / total_requirements * 100
        if total_requirements
        else 100.0
    )

    return {
        "total_requirements": total_requirements,
        "preserved_requirements": preserved_requirements,
        "lost_requirements": lost_requirements,
        "preservation_rate": round(
            preservation_rate,
            2
        ),
        "results": results
    }

def evaluate_errors(
    original_errors: list[str],
    compressed_text: str,
    threshold: float = 0.50
) -> dict:

    compressed_keywords = extract_keywords(
        compressed_text
    )

    results = []

    for error in original_errors:

        error_keywords = extract_keywords(error)

        if not error_keywords:
            continue

        matched_keywords = (
            error_keywords
            & compressed_keywords
        )

        overlap = (
            len(matched_keywords)
            / len(error_keywords)
        )

        preserved = overlap >= threshold

        results.append({
            "error": error,
            "preserved": preserved,
            "overlap": round(overlap, 2),
            "matched_keywords": sorted(
                matched_keywords
            )
        })

    total_errors = len(results)

    preserved_errors = sum(
        1
        for result in results
        if result["preserved"]
    )

    lost_errors = (
        total_errors
        - preserved_errors
    )

    preservation_rate = (
        preserved_errors
        / total_errors * 100
        if total_errors
        else 0.0
    )

    return {
        "total_errors": total_errors,
        "preserved_errors": preserved_errors,
        "lost_errors": lost_errors,
        "preservation_rate": round(
            preservation_rate,
            2
        ),
        "results": results
    }


TODO_SYNONYMS = {
    "modulenotfounderror": {"module", "import", "error"},
    "filenotfounderror": {"file", "not", "found", "error"},
    "fix": {"resolve", "repair", "correct", "fix"},
    "add": {"implement", "create", "add"},
    "train": {"training", "train"},
    "splitting": {"split", "splitting"}
}
def evaluate_todos(
    original_todos: list[str],
    compressed_text: str,
    threshold: float = 0.50
) -> dict:

    compressed_keywords = extract_keywords(compressed_text)

    semantic_groups = {
        "split": {"split", "splitting"},
        "check": {"check", "checking", "verify", "verifying"},
        "leakage": {"leakage", "leak", "contamination"},
        "implement": {"implement", "implementing", "implementation"},
        "train": {"train", "training"},
        "chronological": {"chronological", "temporal", "time"}
    }

    results = []

    def words_match(word1: str, word2: str) -> bool:

        if word1 == word2:
            return True

        for group in semantic_groups.values():

            if word1 in group and word2 in group:
                return True

        if len(word1) >= 4 and len(word2) >= 4:

            if word1.startswith(word2[:4]):
                return True

            if word2.startswith(word1[:4]):
                return True

        return False

    for todo in original_todos:

        todo_keywords = extract_keywords(todo)

        if not todo_keywords:
            continue

        matched_keywords = set()

        for keyword in todo_keywords:

            for compressed_word in compressed_keywords:

                if words_match(
                    keyword,
                    compressed_word
                ):
                    matched_keywords.add(keyword)
                    break

        overlap = (
            len(matched_keywords)
            / len(todo_keywords)
        )

        preserved = overlap >= threshold

        results.append({
            "todo": todo,
            "preserved": preserved,
            "overlap": round(overlap, 2),
            "matched_keywords": sorted(
                matched_keywords
            )
        })

    total_todos = len(results)

    preserved_todos = sum(
        1
        for result in results
        if result["preserved"]
    )

    lost_todos = (
        total_todos
        - preserved_todos
    )

    preservation_rate = (
        preserved_todos
        / total_todos * 100
        if total_todos
        else 100.0
    )

    return {
        "total_todos": total_todos,
        "preserved_todos": preserved_todos,
        "lost_todos": lost_todos,
        "preservation_rate": round(
            preservation_rate,
            2
        ),
        "results": results
    }

def evaluate_code_context(
    original_code_context: dict,
    compressed_text: str,
    threshold: float = 0.50
) -> dict:

    compressed_keywords = extract_keywords(
        compressed_text
    )

    results = []

    fields = [
        "language",
        "file_paths",
        "functions",
        "classes",
        "errors"
    ]

    for field in fields:

        values = original_code_context.get(
            field,
            []
        )

        if isinstance(values, str):
            values = [values]

        for value in values:

            if not value:
                continue

            if str(value).strip().lower() in {
                "unknown",
                "none",
                "null"
            }:
                continue

            value_keywords = extract_keywords(
                value
            )

            if not value_keywords:
                continue

            matched_keywords = (
                value_keywords
                & compressed_keywords
            )

            overlap = (
                len(matched_keywords)
                / len(value_keywords)
            )

            preserved = overlap >= threshold

            results.append({
                "field": field,
                "value": value,
                "preserved": preserved,
                "overlap": round(overlap, 2),
                "matched_keywords": sorted(
                    matched_keywords
                )
            })

    total_items = len(results)

    preserved_items = sum(
        1
        for result in results
        if result["preserved"]
    )

    lost_items = (
        total_items
        - preserved_items
    )

    preservation_rate = (
        preserved_items
        / total_items * 100
        if total_items
        else 0.0
    )

    return {
        "total_items": total_items,
        "preserved_items": preserved_items,
        "lost_items": lost_items,
        "preservation_rate": round(
            preservation_rate,
            2
        ),
        "results": results
    }

def detect_information_loss(
    requirements_result: dict,
    errors_result: dict,
    todos_result: dict,
    code_result: dict
) -> dict:

    categories = {
        "requirements": requirements_result,
        "errors": errors_result,
        "todos": todos_result,
        "code_context": code_result
    }

    category_results = {}
    total_items = 0
    total_preserved = 0
    total_lost = 0

    for category, result in categories.items():

        if category == "requirements":
            total = result.get(
                "total_requirements", 0
            )
            preserved = result.get(
                "preserved_requirements", 0
            )
            lost = result.get(
                "lost_requirements", 0
            )

        elif category == "errors":
            total = result.get(
                "total_errors", 0
            )
            preserved = result.get(
                "preserved_errors", 0
            )
            lost = result.get(
                "lost_errors", 0
            )

        elif category == "todos":
            total = result.get(
                "total_todos", 0
            )
            preserved = result.get(
                "preserved_todos", 0
            )
            lost = result.get(
                "lost_todos", 0
            )

        else:
            total = result.get(
                "total_items", 0
            )
            preserved = result.get(
                "preserved_items", 0
            )
            lost = result.get(
                "lost_items", 0
            )

        total_items += total
        total_preserved += preserved
        total_lost += lost

        category_results[category] = {
            "total": total,
            "preserved": preserved,
            "lost": lost,
            "loss_detected": lost > 0
        }

    information_preservation_rate = (
        total_preserved
        / total_items * 100
        if total_items
        else 0.0
    )

    information_loss_rate = (
        total_lost
        / total_items * 100
        if total_items
        else 0.0
    )

    return {
        "total_items": total_items,
        "preserved_items": total_preserved,
        "lost_items": total_lost,
        "information_preservation_rate": round(
            information_preservation_rate,
            2
        ),
        "information_loss_rate": round(
            information_loss_rate,
            2
        ),
        "loss_detected": total_lost > 0,
        "categories": category_results
    }

def evaluate_overall_quality(
    requirements_result: dict,
    errors_result: dict,
    todos_result: dict,
    code_result: dict,
    information_loss_result: dict
) -> dict:

    category_results = {
        "requirements": requirements_result,
        "errors": errors_result,
        "todos": todos_result,
        "code_context": code_result
    }

    preservation_rates = {}
    active_rates = []

    for category, result in category_results.items():

        if category == "requirements":
            total = result.get("total_requirements", 0)
            rate = result.get("preservation_rate", 100.0)

        elif category == "errors":
            total = result.get("total_errors", 0)
            rate = result.get("preservation_rate", 100.0)

        elif category == "todos":
            total = result.get("total_todos", 0)
            rate = result.get("preservation_rate", 100.0)

        else:
            total = result.get("total_items", 0)
            rate = result.get("preservation_rate", 100.0)

        if total == 0:
            preservation_rates[category] = 100.0
        else:
            preservation_rates[category] = rate
            active_rates.append(rate)

    overall_preservation = (
        sum(active_rates) / len(active_rates)
        if active_rates
        else 100.0
    )

    information_loss_rate = information_loss_result.get(
        "information_loss_rate",
        0.0
    )

    quality_score = (
        overall_preservation
        - information_loss_rate
    )

    quality_score = max(
        0.0,
        min(100.0, quality_score)
    )

    if quality_score >= 90:
        quality_level = "Excellent"
    elif quality_score >= 75:
        quality_level = "Good"
    elif quality_score >= 60:
        quality_level = "Moderate"
    else:
        quality_level = "Poor"

    return {
        "quality_score": round(
            quality_score,
            2
        ),
        "quality_level": quality_level,
        "overall_preservation_rate": round(
            overall_preservation,
            2
        ),
        "information_loss_rate": round(
            information_loss_rate,
            2
        ),
        "category_preservation": preservation_rates
    }

