import re
from typing import List, Dict


# ============================================================
# PHASE 4 — TEXT PREPROCESSING
# ============================================================

def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.strip()
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def detect_code(text: str) -> bool:
    code_patterns = [
        r"```",
        r"\bdef\s+\w+\s*\(",
        r"\bclass\s+\w+",
        r"\bimport\s+\w+",
        r"\bfrom\s+\w+\s+import\s+",
        r"\bpublic\s+class\s+\w+",
        r"\bSystem\.out\.println\s*\(",
        r"\bconsole\.log\s*\("
    ]

    for pattern in code_patterns:
        if re.search(pattern, text):
            return True

    return False


def estimate_tokens(text: str) -> int:
    word_count = len(text.split())
    return round(word_count * 1.3)


def classify_message(message: Dict) -> Dict:
    content = message["content"].lower()

    categories = []

    if message["has_code"]:
        categories.append("code")

    error_keywords = [
        "error",
        "exception",
        "traceback",
        "failed",
        "failure",
        "bug",
        "issue",
        "not working",
        "module not found",
        "modulenotfounderror",
        "nullpointerexception",
        "syntaxerror",
        "typeerror",
        "valueerror"
    ]

    if any(keyword in content for keyword in error_keywords):
        categories.append("error")

    requirement_keywords = [
        "need",
        "needs",
        "want",
        "wants",
        "must",
        "should",
        "required",
        "banana hai",
        "karna hai",
        "hona chahiye",
        "chahiye"
    ]

    if any(keyword in content for keyword in requirement_keywords):
        categories.append("requirement")

    preference_keywords = [
        "prefer",
        "preference",
        "i like",
        "i don't like",
        "mujhe pasand",
        "mujhe nahi pasand",
        "mujhe simple",
        "mujhe easy"
    ]

    if any(keyword in content for keyword in preference_keywords):
        categories.append("preference")

    decision_keywords = [
        "decided",
        "final",
        "we will use",
        "hum use karenge",
        "ye use karenge",
        "start karenge",
        "final karte hain"
    ]

    if any(keyword in content for keyword in decision_keywords):
        categories.append("decision")

    todo_keywords = [
        "next step",
        "todo",
        "next",
        "later",
        "baad mein",
        "agla step"
    ]

    if any(keyword in content for keyword in todo_keywords):
        categories.append("todo")

    if not categories:
        categories.append("general")

    return {
        **message,
        "categories": categories
    }


# ============================================================
# PHASE 5 — CODE-AWARE PROCESSING
# ============================================================

def extract_code_blocks(text: str) -> List[Dict]:
    pattern = r"```([a-zA-Z0-9_+#.-]*)\n?(.*?)```"

    matches = re.findall(
        pattern,
        text,
        flags=re.DOTALL
    )

    blocks = []

    for index, match in enumerate(matches, start=1):
        language = match[0].strip().lower()
        code = match[1].strip()

        blocks.append({
            "block_id": index,
            "language": language if language else "unknown",
            "content": code,
            "line_count": len(code.splitlines())
        })

    return blocks


def detect_programming_language(text: str) -> str:
    lower_text = text.lower()

    if re.search(r"\bimport\s+(numpy|pandas|sklearn|tensorflow|torch|fastapi)\b", lower_text):
        return "python"

    if re.search(r"\b(def|elif|print|self)\b", lower_text):
        return "python"

    if re.search(r"\bpublic\s+(class|static)\b", lower_text):
        return "java"

    if re.search(r"\bsystem\.out\.println\s*\(", lower_text):
        return "java"

    if re.search(r"\b(const|let|var)\s+\w+\s*=", lower_text):
        return "javascript"

    if re.search(r"\bconsole\.log\s*\(", lower_text):
        return "javascript"

    if re.search(r"#include\s*<[^>]+>", lower_text):
        return "cpp"

    if re.search(r"\bSELECT\b.+\bFROM\b", text, re.IGNORECASE | re.DOTALL):
        return "sql"

    if re.search(r"\b(SELECT|INSERT|UPDATE|DELETE)\b", text, re.IGNORECASE):
        return "sql"

    return "unknown"


def extract_file_paths(text: str) -> List[str]:
    patterns = [
        r"[A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]+",
        r"(?:\./|\.\./|/)[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*",
        r"\b[A-Za-z0-9_.\-]+\.(?:py|java|js|ts|tsx|jsx|json|csv|txt|md|html|css|sql|ipynb)\b"
    ]

    paths = []

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            if match not in paths:
                paths.append(match)

    return paths


def extract_functions_and_classes(text: str) -> Dict:
    functions = []
    classes = []

    function_patterns = [
        r"\bdef\s+([A-Za-z_]\w*)\s*\(",
        r"\b(?:public|private|protected)?\s*(?:static\s+)?[\w<>\[\]]+\s+([A-Za-z_]\w*)\s*\("
    ]

    class_patterns = [
        r"\bclass\s+([A-Za-z_]\w*)",
        r"\bpublic\s+class\s+([A-Za-z_]\w*)"
    ]

    for pattern in function_patterns:
        for match in re.findall(pattern, text):
            if match not in functions:
                functions.append(match)

    for pattern in class_patterns:
        for match in re.findall(pattern, text):
            if match not in classes:
                classes.append(match)

    return {
        "functions": functions,
        "classes": classes
    }


def extract_error_details(text: str) -> List[str]:
    error_patterns = [
        r"\b[A-Za-z_][A-Za-z0-9_]*(?:Error|Exception)\b",
        r"\b(?:ERROR|Error|Exception|Traceback)[^\n]*"
    ]

    errors = []

    for pattern in error_patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            match = match.strip()

            if match and match not in errors:
                errors.append(match)

    return errors


def analyze_code(text: str) -> Dict:
    code_blocks = extract_code_blocks(text)
    language = detect_programming_language(text)
    file_paths = extract_file_paths(text)
    symbols = extract_functions_and_classes(text)
    errors = extract_error_details(text)

    return {
        "is_code": detect_code(text),
        "language": language,
        "code_blocks": code_blocks,
        "file_paths": file_paths,
        "functions": symbols["functions"],
        "classes": symbols["classes"],
        "errors": errors
    }


def calculate_importance(message: Dict) -> float:
    score = 0.1

    category_weights = {
        "error": 0.30,
        "requirement": 0.25,
        "decision": 0.25,
        "todo": 0.20,
        "code": 0.20,
        "preference": 0.15,
        "general": 0.0
    }

    for category in message["categories"]:
        score += category_weights.get(category, 0.0)

    if message["role"] == "user":
        score += 0.05

    score = min(score, 1.0)

    return round(score, 2)


# ============================================================
# MESSAGE PREPROCESSING
# ============================================================

def preprocess_messages(messages: List[Dict]) -> List[Dict]:
    processed_messages = []

    for index, message in enumerate(messages, start=1):
        role = message.get("role", "").strip().lower()
        content = message.get("content", "")

        cleaned_content = normalize_text(content)

        if not cleaned_content:
            continue

        word_count = len(cleaned_content.split())

        processed_message = {
            "message_id": index,
            "role": role,
            "content": cleaned_content,
            "has_code": detect_code(cleaned_content),
            "character_count": len(cleaned_content),
            "word_count": word_count,
            "estimated_tokens": estimate_tokens(cleaned_content)
        }

        processed_message = classify_message(processed_message)

        processed_message["code_analysis"] = analyze_code(
            cleaned_content
        )

        processed_message["importance_score"] = calculate_importance(
            processed_message
        )

        processed_messages.append(processed_message)

    return processed_messages


# ============================================================
# CONVERSATION ANALYSIS
# ============================================================

def analyze_conversation(messages: List[Dict]) -> Dict:
    total_words = sum(
        message["word_count"]
        for message in messages
    )

    total_tokens = sum(
        message["estimated_tokens"]
        for message in messages
    )

    user_messages = sum(
        1 for message in messages
        if message["role"] == "user"
    )

    assistant_messages = sum(
        1 for message in messages
        if message["role"] == "assistant"
    )

    code_messages = sum(
        1 for message in messages
        if message["has_code"]
    )

    category_counts = {
        "error": 0,
        "requirement": 0,
        "decision": 0,
        "todo": 0,
        "code": 0,
        "preference": 0,
        "general": 0
    }

    for message in messages:
        for category in message["categories"]:
            if category in category_counts:
                category_counts[category] += 1

    important_messages = [
        message
        for message in messages
        if message["importance_score"] >= 0.40
    ]

    high_importance_messages = [
        message
        for message in messages
        if message["importance_score"] >= 0.60
    ]

    context = {
        "requirements": [],
        "decisions": [],
        "errors": [],
        "todos": [],
        "preferences": [],
        "code_messages": []
    }

    for message in messages:

        item = {
            "message_id": message["message_id"],
            "role": message["role"],
            "content": message["content"],
            "importance_score": message["importance_score"]
        }

        categories = message["categories"]

        if "requirement" in categories:
            context["requirements"].append(item)

        if "decision" in categories:
            context["decisions"].append(item)

        if "error" in categories:
            context["errors"].append(item)

        if "todo" in categories:
            context["todos"].append(item)

        if "preference" in categories:
            context["preferences"].append(item)

        if "code" in categories:
            context["code_messages"].append(item)

    return {
        "total_messages": len(messages),
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "total_words": total_words,
        "estimated_tokens": total_tokens,
        "code_messages": code_messages,
        "category_counts": category_counts,
        "important_messages": len(important_messages),
        "high_importance_messages": len(high_importance_messages),
        "context": context
    }
