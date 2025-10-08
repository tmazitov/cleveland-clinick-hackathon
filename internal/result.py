from internal.database import *
from internal.services.embedding.embedding import embedding
from internal.services.doctors_provider.doctors_provider import *
from openai import OpenAI

class Result:
    def __init__(self, client: OpenAI, db: Database):
        self.client = client
        self.db = db

    async def find_doctors(self, symptoms: List[str], user_id: int):
        closest_symptom_list = []

        # Vectorize and find closest symptoms
        for s in symptoms:
            print(f"info : symptom - {s} proccessing...")
            symptom_vector = embedding(text=s, client=self.client)
            closest_symptom = self.db.find_closest(symptom_vector)[0]
            closest_symptom_list.append(closest_symptom)

        closest_symptom_list.sort(key=lambda x: x[3])
        print("Closest symptom:", closest_symptom_list)

        # Trying to find doctors for closest symptoms
        doctors = []
        for s in closest_symptom_list:
            uuid = s[2]
            doctors = await get_doctors(uuid)
            if doctors is not None and len(doctors) > 0:
                break

        return doctors
