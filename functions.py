import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

personal_api_key = os.getenv("PERSONAL_API_KEY")
open_ai_api_key = os.getenv("OPENAI_API_KEY")


def get_token():
    payload = {"apikey": '9909a234-1b28-454c-ab8d-f46b0cef7fcf'}
    response = requests.post('https://zadania.aidevs.pl/token/functions', json=payload)
    return response.json().get('token')


def get_task():
    token = get_token()
    response = requests.get(f'https://zadania.aidevs.pl/task/{token}')
    return response.json()


def send_answer():
    token = get_token()
    answer = {
			"name": "addUser",
			"description": "Adding user to database",
			"parameters": {
				"type": "object",
				"properties": {
					"name": {
						"type": "string",
						"description": "User name"
					},
					"surname": {
						"type": "string",
						"description": "User surname",
					},
					"year": {
						"type": "integer",
						"description": "User year of birth",
					}
				},
				"required": [
					"type", "tags", "command"
				]
			}
		}
    payload = {"answer": answer}
    response = requests.post(f'https://zadania.aidevs.pl/answer/{token}', json=payload)
    return response.json()


print(send_answer())