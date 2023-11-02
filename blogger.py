import requests
from dotenv import load_dotenv
import os

load_dotenv()

personal_api_key = os.getenv("PERSONAL_API_KEY")
open_ai_api_key = os.getenv("OPENAI_API_KEY")


def get_token():
    payload = {"apikey": personal_api_key}
    response = requests.post('https://zadania.aidevs.pl/token/blogger', json=payload)
    return response.json().get('token')


def get_task():
    token = get_token()
    response = requests.get(f'https://zadania.aidevs.pl/task/{token}')
    return response.json()['blog'], token

def get_completion():
    topics, token = get_task()
    articles_list = []

    for topic in topics:
        content = f'Tworzysz artykuł na bloga na temat przyrzadzania pizyy Margherity. Napisz krotki artykul dla rozdzialu pod tytulem: {topic}. Odpowiedz tylko trescia artykulu (bez tytulu), niczym wiecej'
        data = {"messages": [{"role": "user", "content": content}], "model": "gpt-3.5-turbo"}
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + open_ai_api_key}
        response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
        parsed_response = response.json()['choices'][0]['message']['content']
        articles_list.append(parsed_response)
    return (articles_list, token)


def send_answer():
    articles_list, token = get_completion()
    payload = {"answer":articles_list}
    response = requests.post(f'https://zadania.aidevs.pl/answer/{token}', json=payload)
    return response.json()


print(send_answer())