import requests
from dotenv import load_dotenv
import os

load_dotenv()

personal_api_key = os.getenv("PERSONAL_API_KEY")
open_ai_api_key = os.getenv("OPENAI_API_KEY")


def get_token():
    payload = {"apikey": personal_api_key}
    response = requests.post('https://zadania.aidevs.pl/token/moderation', json=payload)
    return response.json().get('token')


def get_task():
    token = get_token()
    response = requests.get(f'https://zadania.aidevs.pl/task/{token}')
    return response.json()['input'], token


def check_openai():
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + open_ai_api_key}
    prompt_list, token = get_task()
    response_list = []
    for prompt in prompt_list:
        data = {"input":prompt}
        response = requests.post('https://api.openai.com/v1/moderations', json=data, headers=headers)
        flagged = response.json()['results'][0]['flagged']
        response_list.append(1) if flagged else response_list.append(0)
    return response_list, token


def send_answer():
    response_list, token = check_openai()
    payload = {"answer":response_list}
    response = requests.post(f'https://zadania.aidevs.pl/answer/{token}', json=payload)
    return response.json()

print(send_answer())