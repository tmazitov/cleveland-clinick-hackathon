import os
import sys
import json
import openai, dotenv

parent_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder_path)

from internal.database import Database
from internal.services.embedding.embedding import embedding

KEY = dotenv.get_key(dotenv_path=f'{parent_folder_path}/.env', key_to_get='OPENAI_API_KEY')

client = openai.OpenAI(api_key=KEY)
db_client = Database(f"{parent_folder_path}/symptoms.db")

# with open(f'{parent_folder_path}/tools/symptoms.json', 'r') as f:
#     symptoms = json.load(f)
#     counter = 0
#     for symptom in symptoms:
#         name = symptom['name']
#         value = symptom['value']
#         # embedding_vector = embedding(name, client)
#         # db_client.add_vector(name=name, vector=embedding_vector, uuid=value)
#         counter += 1
#         print(f"Added {counter}: {name} - {value}")
#
# db_client.close()




