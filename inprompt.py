import requests
from dotenv import load_dotenv
import os

load_dotenv()

personal_api_key = os.getenv("PERSONAL_API_KEY")
open_ai_api_key = os.getenv("OPENAI_API_KEY")


def get_token():
    payload = {"apikey": personal_api_key}
    response = requests.post('https://zadania.aidevs.pl/token/inprompt', json=payload)
    return response.json().get('token')


def get_task():
    token = get_token()
    response = requests.get(f'https://zadania.aidevs.pl/task/{token}')
    response = response.json()
    return response, token


def filter_response():
    response, token = get_task()
    sentences = response['input']
    question = response['question'][:-1]
    name = question.split()[-1]
    sentence = ''.join([sentence for sentence in sentences if name in sentence])
    return question, sentence, token


def get_answer():
    question, sentence, token = filter_response()
    content = f'Your task is to answer the question based on a sentence. Question: {question}. Sentence: {sentence} '
    data = {"messages": [{"role": "user", "content": content}], "model": "gpt-3.5-turbo"}
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + open_ai_api_key}
    response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
    parsed_response = response.json()['choices'][0]['message']['content']
    return parsed_response, token


def send_answer():
    answer, token = get_answer()
    payload = {"answer":answer}
    response = requests.post(f'https://zadania.aidevs.pl/answer/{token}', json=payload)
    return response.json()


print(send_answer())