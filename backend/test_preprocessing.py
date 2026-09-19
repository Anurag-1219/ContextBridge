from preprocessing import preprocess_messages


sample_conversation = [
    {
        "role": "user",
        "content": "   Mujhe   machine learning project banana hai.   "
    },
    {
        "role": "assistant",
        "content": "Haan, tum predictive maintenance project bana sakte ho."
    },
    {
        "role": "user",
        "content": "Python code bhi chahiye:\n```python\nprint('Hello ML')\n```"
    }
]


result = preprocess_messages(sample_conversation)

for message in result:
    print(message)
