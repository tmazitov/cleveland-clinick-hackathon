# import pytest
import openai
import sys
sys.path.append('/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot')
from requester import Requester
from parser_.parser_manager import Parser
import dotenv
# from database import Database
def test_parser():
    parser = Parser()
    client = openai.Client(api_key=dotenv.get_key(dotenv_path='/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot/.env', key_to_get='OPENAI_API_KEY'))
    requester = Requester(client)
    response = requester.request(user_request='Igor')
    parsed_response = parser.parse(response)
    # DB_instance = Database()
    # DB_instance.add_vector(name='Igor', vector=parsed_response)
    # DB_instance.close()
    # assert True is True

if __name__ == '__main__':
    test_parser()
