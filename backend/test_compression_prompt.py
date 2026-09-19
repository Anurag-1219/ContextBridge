from compression import build_compression_input, build_compression_prompt

sample_messages = [
    {
        "message_id": 1,
        "role": "user",
        "content": "Mujhe Python ML project banana hai.",
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
        "role": "user",
        "content": "ModuleNotFoundError aa raha hai.",
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
    }
]

compression_input = build_compression_input(sample_messages)

prompt = build_compression_prompt(compression_input)

print("=== COMPRESSION PROMPT ===")
print(prompt)

print("")
print("======================================")
print("PHASE 6.2 COMPLETE")
print("======================================")
