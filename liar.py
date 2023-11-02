import requests
from dotenv import load_dotenv
import os

load_dotenv()

personal_api_key = os.getenv("PERSONAL_API_KEY")
open_ai_api_key = os.getenv("OPENAI_API_KEY")


def get_token():
    payload = {"apikey": personal_api_key}
    response = requests.post('https://zadania.aidevs.pl/token/liar', json=payload)
    return response.json().get('token')


def get_task():
    token = get_token()
    question = 'What is the capital of Poland?'
    response = requests.post(f'https://zadania.aidevs.pl/task/{token}', data={'question': question})
    answer = response.json()['answer']
    return question, answer, token


def guardrails():
    question, answer, token = get_task()
    content = f'Your task is to check if answer is connected to the provided question. Reply only YES or NO. Question: {question}. Answer: {answer} '
    data = {"messages": [{"role": "user", "content": content}], "model": "gpt-3.5-turbo"}
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + open_ai_api_key}
    response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
    parsed_response = response.json()['choices'][0]['message']['content']
    return parsed_response, token


def send_answer():
    answer, token = guardrails()
    payload = {"answer": answer}
    response = requests.post(f'https://zadania.aidevs.pl/answer/{token}', json=payload)
    return response.json()


print(send_answer())