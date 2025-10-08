import sys, os
import openai

parent_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder_path)

from internal.services.doctors_provider.doctors_provider import DoctorsProvider

def main():
    provider = DoctorsProvider()

    doctors = provider.get_doctors(symptomUUID="5158dc1a-de9f-48f4-a792-4f02afe4585c")

    print(f"Found {len(doctors)} doctors:")
    for doc in doctors:
        print("-", doc)

    provider.close()


if __name__ == '__main__':
    main()