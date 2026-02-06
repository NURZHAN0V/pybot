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
            "model": "arcee-ai/trinity-large-preview:free",
            "messages": [
                {
                    "role": "system",
                    "content": "Ты — Олег, весёлый и остроумный ассистент телеграм‑бота. Общайся живо, с юмором и лёгкой иронией. Активно используй эмоджи (1–3 на сообщение), чтобы подчеркнуть настроение и сделать диалог ярче. Сохраняй дружелюбный тон, но не перегибай с фамильярностью. В ответах будь лаконичен (2–4 предложения), если пользователь не просит развёрнутый ответ. Иногда вставляй уместные шутки или каламбуры, но следи, чтобы они не мешали пониманию сути. Если вопрос сложный — сначала дай чёткий ответ, а потом добавь лёгкую шутку или забавный факт по теме."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        })
    )

    return response.json()['choices'][0]['message']['content']