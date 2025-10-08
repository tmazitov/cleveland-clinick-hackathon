# import pytest
import openai
import dotenv
import sys, os

parent_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder_path)

from internal.requester.requester import Requester
from internal.parser.parser_manager import Parser
# from database import Database
def test_parser():
    parser = Parser()
    client = openai.Client(api_key=dotenv.get_key(dotenv_path=f'{parent_folder_path}/.env', key_to_get='OPENAI_API_KEY'))
    requester = Requester(client)
    response = requester.send(user_request='Igor')
    parsed_response = parser.parse(response)
    # DB_instance = Database()
    # DB_instance.add_vector(name='Igor', vector=parsed_response)
    # DB_instance.close()
    # assert True is True

if __name__ == '__main__':
    test_parser()
