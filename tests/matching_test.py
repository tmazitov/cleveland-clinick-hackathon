import sys, os
import dotenv
import openai

parent_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder_path)

from internal.database import Database
from internal.services.embedding.embedding import embedding

def main():
    test_input = ("back pain")

    OPEN_AI_API_KEY = dotenv.get_key(dotenv_path=f'{parent_folder_path}/.env', key_to_get='OPENAI_API_KEY')
    client = openai.OpenAI(api_key=OPEN_AI_API_KEY)
    embedding_vector = embedding(test_input, client)
    DB_Instance = Database(f"{parent_folder_path}/symptoms.db")

    print(f"{test_input} - result:", DB_Instance.find_closest(embedding_vector))

    DB_Instance.close()

if __name__ == '__main__':
    main()
