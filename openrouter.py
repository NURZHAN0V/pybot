import requests
import json

def fetch_openrouter_api_key(token, message):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "z-ai/glm-4.5-air:free",
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        })
    )

    return response.json()['choices'][0]['message']['content']