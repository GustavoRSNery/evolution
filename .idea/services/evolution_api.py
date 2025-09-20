import os

import requests

from dotenv import load_dotenv


load_dotenv("D:\Projects\evolution\.env")


class EvolutionAPI:

    BASE_URL = os.getenv('EVO_BASE_URL')
    INSTANCE_NAME = os.getenv('EVO_INSTANCE_NAME')

    def __init__(self):
        self.__api_key = os.getenv('AUTHENTICATION_API_KEY')
        self.__headers = {
            'apikey': self.__api_key,
            'Content-Type': 'application/json'
        }

    def send_message(self, number, text):
        payload = {
            'number': number,
            'text': text,
        }
        response = requests.post(
            url=f'{self.BASE_URL}/message/sendText/{self.INSTANCE_NAME}',
            headers=self.__headers,
            json=payload,
        )
        return response.json()
