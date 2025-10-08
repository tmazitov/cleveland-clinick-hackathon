# import pytest
import openai
import dotenv
import sys, os

parent_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder_path)

from internal.requester.requester import Requester

def requests():
    client = openai.OpenAI(api_key=dotenv.get_key(dotenv_path=f'{parent_folder_path}/.env', key_to_get='OPENAI_API_KEY'))
    requester = Requester(client=client)
    response = requester.send(user_request='Hi! How are you?')
    # assert response is not None
    return response

print(requests())