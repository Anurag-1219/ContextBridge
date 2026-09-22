from preprocessing import preprocess_messages
from context_compression import build_compression_input, compress_with_llm


conversation = [
    {
        "role": "user",
        "content": "Mujhe Python me fraud detection project banana hai."
    },
    {
        "role": "assistant",
        "content": "Hum supervised machine learning use karenge."
    },
    {
        "role": "user",
        "content": "Project me time-aware split aur data leakage avoid karna hai."
    },
    {
        "role": "user",
        "content": "ModuleNotFoundError aa raha hai."
    }
]


processed = preprocess_messages(conversation)

compression_input = build_compression_input(processed)

compressed_context = compress_with_llm(compression_input)

print("\n========== COMPRESSED CONTEXT ==========\n")
print(compressed_context)
