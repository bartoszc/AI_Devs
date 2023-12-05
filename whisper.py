import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

personal_api_key = os.getenv("PERSONAL_API_KEY")
open_ai_api_key = os.getenv("OPENAI_API_KEY")


def get_token():
    payload = {"apikey": '9909a234-1b28-454c-ab8d-f46b0cef7fcf'}
    response = requests.post('https://zadania.aidevs.pl/token/whisper', json=payload)
    return response.json().get('token')


def get_task():
    token = get_token()
    response = requests.get(f'https://zadania.aidevs.pl/task/{token}')
    file = response.json()['msg'].split()[-1]
    return file, token


def get_transcription():
    client = OpenAI()
    file, token = get_task()
    audio_file= open("mateusz.mp3", "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="text")
    return transcript, token


def send_answer():
    transcript, token = get_transcription()
    payload = {"answer": transcript}
    response = requests.post(f'https://zadania.aidevs.pl/answer/{token}', json=payload)
    return response.json()



print(send_answer())
