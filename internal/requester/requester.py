import openai
import sys
sys.path.append('/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot/internal/requester')
from prompts import MASTER_PROMPT
from typing import Any, List, Dict

class Requester:
    def __init__(self, client: openai.OpenAI):
        self.client = client

    def send(self, user_request: str) -> str:
        response = self.client.responses.create(
            model='gpt-5',
            input=[
                {'role': 'system', 'content': MASTER_PROMPT},
                {'role': 'user', 'content': user_request}
            ],
        )
        return response.output_text