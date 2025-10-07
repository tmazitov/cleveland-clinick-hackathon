import openai, dotenv
import json
import database
from services.embedding.embedding import embedding
KEY = dotenv.get_key(dotenv_path='/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot/.env', key_to_get='OPENAI_API_KEY')

client = openai.OpenAI(api_key=KEY)
db_client = database.Database()

with open('symptoms_parser/symptoms.json', 'r') as f:
    symptoms = json.load(f)
    counter = 0
    for symptom in symptoms:
        name = symptom['name']
        value = symptom['value']
        embedding_vector = embedding(name, client)
        db_client.add_vector(name=name, vector=embedding_vector, uuid=value)
        counter += 1
        print(f"Added {counter}: {name} - {value}")

db_client.close()




