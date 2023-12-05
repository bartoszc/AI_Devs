import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from requests.exceptions import HTTPError, ConnectionError, Timeout

load_dotenv()

personal_api_key = os.getenv("PERSONAL_API_KEY")
open_ai_api_key = os.getenv("OPENAI_API_KEY")


def get_token():
    payload = {"apikey": '9909a234-1b28-454c-ab8d-f46b0cef7fcf'}
    response = requests.post('https://zadania.aidevs.pl/token/scraper', json=payload)
    return response.json().get('token')


def get_task():
    token = get_token()
    response = requests.get(f'https://zadania.aidevs.pl/task/{token}')
    message = response.json()['msg']
    article = response.json()['input']
    question = response.json()['question']
    return message, article, question, token


def fetch_article():
    message, article, question, token = get_task()
    try:
        headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}
        response = requests.get(article, headers=headers)
        response.raise_for_status()  

        response_str = response.content.decode('utf-8')
        return message, response_str, question, token

    except HTTPError as http_err:
        if response.status_code == 403:
            return('Access forbidden. Please check your permissions or headers.')
        else:
            return(f'HTTP error occurred: {http_err}') 
    except ConnectionError as conn_err:
        return(f'Error Connecting: {conn_err}')
    except Timeout as timeout_err:
        return(f'Timeout Error: {timeout_err}')
    except Exception as err:
        return(f'Other error occurred: {err}') 


def generate_answer():
    message, article, question, token = fetch_article()
    content = f"""'''system: - {message} ''' Article: {article} Question: {question}"""
    data = {"messages": [{"role": "user", "content": content}], "model": "gpt-4"}
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + open_ai_api_key}
    response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
    parsed_response = response.json()['choices'][0]['message']['content']
    return parsed_response, token


def send_answer():
    answer, token = generate_answer()
    payload = {"answer": answer}
    response = requests.post(f'https://zadania.aidevs.pl/answer/{token}', json=payload)
    return response.json()


print(send_answer())