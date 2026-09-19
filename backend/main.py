from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from preprocessing import preprocess_messages, analyze_conversation


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
