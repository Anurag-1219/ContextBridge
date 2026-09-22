from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

from preprocessing import preprocess_messages, analyze_conversation
from context_compression import build_compression_input, compress_with_llm
from compression_schema import build_compression_schema
from handoff import build_handoff, build_handoff_prompt, validate_handoff
from handoff_metadata import create_handoff_package
from handoff_export import export_handoff_json
from handoff_loader import load_handoff_json, validate_loaded_handoff
from token_metrics import calculate_token_reduction

from context_evaluation import (
    evaluate_requirements,
    evaluate_errors,
    evaluate_todos,
    evaluate_code_context,
    detect_information_loss,
    evaluate_overall_quality
)


app = FastAPI(
    title="ContextBridge API",
    description="Backend for AI-powered conversation context compression and handoff.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Message(BaseModel):
    role: str
    content: str


class ConversationRequest(BaseModel):
    messages: List[Message]


class CompressionRequest(BaseModel):
    messages: List[Dict]


class HandoffExportRequest(BaseModel):
    package: Dict


@app.get("/")
def root():
    return {
        "project": "ContextBridge",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/process-conversation")
def process_conversation(request: ConversationRequest):

    messages = [
        {
            "role": message.role,
            "content": message.content
        }
        for message in request.messages
    ]

    processed_messages = preprocess_messages(messages)

    conversation_stats = analyze_conversation(
        processed_messages
    )

    return {
        "success": True,
        "stats": conversation_stats,
        "messages": processed_messages
    }


def collect_evaluation_context(
    processed_messages: List[Dict]
) -> Dict:

    requirements = []
    errors = []
    todos = []

    code_context = {
        "language": [],
        "file_paths": [],
        "functions": [],
        "classes": [],
        "errors": []
    }

    for message in processed_messages:

        content = message.get("content", "")
        categories = message.get("categories", [])

        if "requirement" in categories:
            requirements.append(content)

        if "error" in categories:
            errors.append(content)

        if "todo" in categories:
            todos.append(content)

        code = message.get("code_analysis", {})

        language = code.get("language")

        if language:
            code_context["language"].append(language)

        for key in [
            "file_paths",
            "functions",
            "classes",
            "errors"
        ]:
            values = code.get(key, [])

            if isinstance(values, str):
                values = [values]

            code_context[key].extend(values)

    for key in code_context:
        code_context[key] = list(
            dict.fromkeys(code_context[key])
        )

    return {
        "requirements": requirements,
        "errors": errors,
        "todos": todos,
        "code_context": code_context
    }


@app.post("/compress-conversation")
def compress_conversation(
    request: CompressionRequest
):

    raw_messages = [
        {
            "role": message.get("role", ""),
            "content": message.get("content", "")
        }
        for message in request.messages
    ]

    processed_messages = preprocess_messages(
        raw_messages
    )

    conversation_stats = analyze_conversation(
        processed_messages
    )

    compression_input = build_compression_input(
        processed_messages
    )

    original_text = "\n".join(
        message.get("content", "")
        for message in raw_messages
    )

    compressed_text = compress_with_llm(
        compression_input
    )

    schema_result = build_compression_schema(
        compressed_text
    )

    if not schema_result["success"]:
        return {
            "success": False,
            "error": "Compression output failed schema validation.",
            "schema": schema_result
        }

    sections = schema_result["sections"]

    handoff = build_handoff(
        sections
    )

    handoff_validation = validate_handoff(
        handoff
    )

    handoff_prompt = build_handoff_prompt(
        handoff
    )

    handoff_package = create_handoff_package(
        handoff
    )

    token_metrics = calculate_token_reduction(
        original_text,
        compressed_text
    )

    evaluation_context = collect_evaluation_context(
        processed_messages
    )

    requirements_result = evaluate_requirements(
        evaluation_context["requirements"],
        sections.get("REQUIREMENTS", "")
    )

    errors_result = evaluate_errors(
        evaluation_context["errors"],
        sections.get("ERRORS / ISSUES", "")
    )

    todos_result = evaluate_todos(
        evaluation_context["todos"],
        sections.get("TODO / NEXT STEPS", "")
    )

    code_result = evaluate_code_context(
        evaluation_context["code_context"],
        sections.get("CODE CONTEXT", "")
    )

    loss_result = detect_information_loss(
        requirements_result,
        errors_result,
        todos_result,
        code_result
    )

    quality_result = evaluate_overall_quality(
        requirements_result,
        errors_result,
        todos_result,
        code_result,
        loss_result
    )

    return {
        "success": True,

        "stats": conversation_stats,

        "compression": {
            "text": compressed_text,
            "schema": schema_result
        },

        "token_metrics": token_metrics,

        "quality": quality_result,

        "evaluation": {
            "requirements": requirements_result,
            "errors": errors_result,
            "todos": todos_result,
            "code_context": code_result,
            "information_loss": loss_result
        },

        "handoff": handoff,

        "handoff_validation": handoff_validation,

        "handoff_package": handoff_package,

        "handoff_prompt": handoff_prompt
    }

@app.post("/export-handoff")
def export_handoff(request: HandoffExportRequest):

    output_path = str(
        Path(__file__).resolve().parent / "contextbridge_handoff.json"
    )

    exported_path = export_handoff_json(
        request.package,
        output_path
    )

    return {
        "success": True,
        "message": "Handoff exported successfully.",
        "file": exported_path
    }

@app.get("/load-handoff")
def load_handoff():

    input_path = str(
        Path(__file__).resolve().parent / "contextbridge_handoff.json"
    )

    package = load_handoff_json(
        input_path
    )

    validation = validate_loaded_handoff(
        package
    )

    return {
        "success": validation["valid"],
        "validation": validation,
        "package": package
    }

