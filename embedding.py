import requests
from dotenv import load_dotenv
import os

load_dotenv()

personal_api_key = os.getenv("PERSONAL_API_KEY")
open_ai_api_key = os.getenv("OPENAI_API_KEY")



def get_token():
    payload = {"apikey": personal_api_key}
    response = requests.post('https://zadania.aidevs.pl/token/embedding', json=payload)
    return response.json().get('token')


def create_embedding():
    token = get_token()
    data = {"input": 'Hawaiian pizza', "model": "text-embedding-ada-002"}
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + open_ai_api_key}
    response = requests.post('https://api.openai.com/v1/embeddings', json=data, headers=headers)
    embedding = response.json()['data'][0]['embedding']
    return embedding, token


def send_answer():
    embedding, token = create_embedding()
    payload = {"answer": embedding}
    response = requests.post(f'https://zadania.aidevs.pl/answer/{token}', json=payload)
    return response.json()


print(send_answer())
