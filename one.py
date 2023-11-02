import requests
from dotenv import load_dotenv
import os

load_dotenv()

personal_api_key = os.getenv("PERSONAL_API_KEY")


def get_token():
    payload = {"apikey":personal_api_key}
    response = requests.post('https://zadania.aidevs.pl/token/helloapi', json=payload)
    return response.json().get('token')


def get_task():
    token = get_token()
    response = requests.get(f'https://zadania.aidevs.pl/task/{token}')
    return token, response.json().get('cookie')


def send_answer():
    token, cookie = get_task()
    payload = {"answer":cookie}
    response = requests.post(f'https://zadania.aidevs.pl/answer/{token}', json=payload)
    return response.json()


print(send_answer())