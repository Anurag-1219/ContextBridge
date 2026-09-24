# ContextBridge

> AI-powered conversation compression and context handoff system for long AI conversations.

ContextBridge is a browser extension + FastAPI backend that extracts a ChatGPT conversation, sends it to a backend, compresses the context using an LLM, evaluates the result, and generates a structured handoff package.

## What Problem Does It Solve?

Long AI conversations contain important information such as objectives, requirements, decisions, preferences, technical constraints, code state, errors, and progress.

ContextBridge converts this conversation into a structured and reusable context package.

## End-to-End Flow

ChatGPT
  ?
Conversation Extraction
  ?
Request Validation
  ?
Preprocessing
  ?
LLM Compression
  ?
Context Evaluation
  ?
Handoff Generation
  ?
Compressed Context
  ?
ContextBridge Popup

## Architecture

### 1. Browser Extension

- content.js extracts the active ChatGPT conversation.
- popup.js sends the extracted conversation to the backend.
- The extension displays the generated compressed context and metrics.

### 2. FastAPI Backend

- Validates incoming requests.
- Validates message roles and content.
- Performs preprocessing and compression.
- Evaluates generated context.
- Generates the structured handoff package.

### 3. LLM Layer

- Local development: Ollama.
- Production: OpenAI API.
- Provider selection is controlled through environment variables.

## Features

- ChatGPT conversation extraction
- Structured context compression
- LLM provider abstraction
- Local Ollama support
- Production OpenAI support
- Request and message validation
- Context quality evaluation
- Structured handoff generation
- Token and compression metrics
- Production FastAPI deployment
- Chrome Manifest V3 extension

## API

### GET /health

Returns the backend health status.

### POST /compress-conversation

Accepts a conversation and returns compressed context, evaluation metrics, and a structured handoff package.

## Security

- API keys are stored only in environment variables.
- Secrets are excluded from Git using .gitignore.
- Incoming messages have role and content validation.
- Request size limits are applied.
- LLM failures are handled as controlled API errors.
- No API key is stored in the browser extension.

## Local Development

Local development uses Ollama.
Production uses the configured OpenAI provider.

Backend:

cd D:\ContextBridge\backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8001

## Browser Extension

1. Enable Developer Mode in Chrome or Brave.
2. Select Load unpacked.
3. Select the ContextBridge extension folder.
4. Open a ChatGPT conversation.
5. Open ContextBridge.
6. Run Compress Conversation.

## Project Structure

ContextBridge/
+-- backend/
¦   +-- main.py
¦   +-- llm_service.py
¦   +-- context_compression.py
¦   +-- context_evaluation.py
¦   +-- handoff.py
¦   +-- requirements.txt
+-- extension/
¦   +-- content.js
¦   +-- popup.js
¦   +-- popup.html
¦   +-- style.css
¦   +-- manifest.json
+-- README.md
