import openai
import datetime

def embedding(text: str, client: openai.OpenAI) -> list:
    response = client.embeddings.create(
        model='text-embedding-3-small',
        input=text
    )
    return response.data[0].embedding
