import openai
from PROMPT import *
from typing import Any, List, Dict

class Requester:
    def __init__(self, client: openai.OpenAI):
        self.client = client

    def request(self, user_request:str ):
        response = self.client.responses.create(
            model='gpt-5',
            input=[
                {'role': 'system',
                 'content': f'{MASTER_PROMPT}'},
                {'role': 'user',
                 'content': f'{user_request}'}
            ],
        )
        return response.output_text