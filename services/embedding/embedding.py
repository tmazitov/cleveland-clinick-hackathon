import openai
import datetime

def embedding(text: str, client: openai.OpenAI) -> list:
    response = client.embeddings.create(
        model='text-embedding-3-small',
        input=text
    )
    return response.data[0].embedding

# def l2_to_percent(l2_distance: float) -> float:
#     return (1 - l2_distance / 2) * 100

if __name__ == '__main__':
    import dotenv
    import sys
    sys.path.append('/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot')
    import database

    client = openai.OpenAI(api_key=dotenv.get_key(dotenv_path='/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot/.env', key_to_get='OPENAI_API_KEY'))
    text = ("back pain")
    # print(datetime.datetime.now())
    embedding_vector = embedding(text, client)
    # print(datetime.datetime.now())
    DB_Instance = database.Database()
    # DB_Instance.add_vector(name=text, vector=embedding_vector)

    # probability_items = [
    #     {
    #         "id" : item[0],
    #         "name" : item[1],
    #         "similarity" : f"{l2_to_percent(item[2])}%",
    #     }
    #     for item in DB_Instance.find_closest(embedding_vector)
    # ]
    print(f"{text} - result:", DB_Instance.find_closest(embedding_vector))

    DB_Instance.close()

    # print(embedding_vector)