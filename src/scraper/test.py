from model_loader_engine import get_client_instance

client = get_client_instance()

response = client.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": (
                "Return ONLY valid JSON. "
                "Do not explain anything. "
                "Return exactly one JSON object."
            ),
        },
        {
            "role": "user",
            "content": "There is no physical address on this page."
        }
    ],
    max_tokens=100,
)

print(response["choices"][0]["message"]["content"])