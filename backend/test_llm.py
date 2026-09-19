from llm_service import compress_conversation


sample_messages = [
    {
        "message_id": 1,
        "role": "user",
        "content": "Mujhe Python me machine learning project banana hai.",
        "importance_score": 0.40,
        "categories": ["requirement"],
        "code_analysis": {
            "is_code": False,
            "language": "unknown",
            "code_blocks": [],
            "file_paths": [],
            "functions": [],
            "classes": [],
            "errors": []
        }
    },
    {
        "message_id": 2,
        "role": "assistant",
        "content": "Tum predictive maintenance project bana sakte ho.",
        "importance_score": 0.10,
        "categories": ["general"],
        "code_analysis": {
            "is_code": False,
            "language": "unknown",
            "code_blocks": [],
            "file_paths": [],
            "functions": [],
            "classes": [],
            "errors": []
        }
    },
    {
        "message_id": 3,
        "role": "user",
        "content": "Mujhe ModuleNotFoundError aa raha hai.",
        "importance_score": 0.45,
        "categories": ["error"],
        "code_analysis": {
            "is_code": False,
            "language": "unknown",
            "code_blocks": [],
            "file_paths": [],
            "functions": [],
            "classes": [],
            "errors": ["ModuleNotFoundError"]
        }
    },
    {
        "message_id": 4,
        "role": "user",
        "content": """Data load karne ke liye ye function hai:

```python
def load_data():
    return "data"
```""",
        "importance_score": 0.35,
        "categories": ["code"],
        "code_analysis": {
            "is_code": True,
            "language": "python",
            "code_blocks": [
                {
                    "block_id": 1,
                    "language": "python",
                    "content": 'def load_data():\n    return "data"',
                    "line_count": 2
                }
            ],
            "file_paths": [],
            "functions": ["load_data"],
            "classes": [],
            "errors": []
        }
    }
]


print("Sending conversation to LLM...")
print("")

result = compress_conversation(sample_messages)

print("=== COMPRESSED CONTEXT ===")
print(result["compressed_context"])

print("")
print("======================================")
print("PHASE 6.3.2 COMPLETE")
print("======================================")
