import requests

def fetch_draft(prompt, api_key, url):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    params = {
        "ai": {
            "model": "gigachat-lite",
            "temperature": 0.9,
            "top_p": 1.0
        },
        "type": "out_image",
        "response_format": "url",
        "content": prompt
    }

    response = requests.post(url, json=params, headers=headers)
    response = response.json()

    if response.get("error"):
        print(response['details'][0]['error_text'])

    task_id = response.get("task_id")
    
    if task_id:
        import time
        # print(task_id)
        image_url = None
        while True:
            image_url = fetch_draft_status(task_id, api_key)
            status = image_url['contents']['status']
            # print(status)
            if status == 2:
                break
            time.sleep(3)

        # print(image_url)
        return image_url['contents']['files'][0]['data']

def fetch_draft_status(task_id, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    url = f'https://ai.mitup.ru/api/v2/status/{task_id}'

    response = requests.get(url, headers=headers)
    return response.json()