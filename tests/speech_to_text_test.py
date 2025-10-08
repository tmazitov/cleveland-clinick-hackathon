import sys, os
import dotenv
import openai

parent_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder_path)

from services.sp_2_tx.sp_2_tx import SpeechToText
from settings import MEDIA

def test_speech_to_text():
    client = openai.OpenAI(api_key=dotenv.get_key(dotenv_path=f'{parent_folder_path}/.env', key_to_get='OPENAI_API_KEY'))
    stt = SpeechToText(client=client)
    result = stt.transcribe(audio_path=f'{MEDIA}/voice_13.wav')
    print(result)
    assert isinstance(result, str)

# if __name__ == '__main__':
#     test_speech_to_text()