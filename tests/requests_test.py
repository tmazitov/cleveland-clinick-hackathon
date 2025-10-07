# import pytest
import sys
sys.path.append('/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot')
from requester import Requester
import openai
import dotenv

def requests():
    client = openai.OpenAI(api_key=dotenv.get_key(dotenv_path='/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot/.env', key_to_get='OPENAI_API_KEY'))
    requester = Requester(client=client)
    response = requester.request(user_request='Hi! How are you?')
    # assert response is not None
    return response

print(requests())