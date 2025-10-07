import sys
sys.path.append("/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot")
from services.sp_2_tx.sp_2_tx import SpeechToText
import dotenv
import openai

def test_speech_to_text():
    client = openai.OpenAI(api_key=dotenv.get_key(dotenv_path='/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot/.env', key_to_get='OPENAI_API_KEY'))
    stt = SpeechToText(client=client)
    result = stt.transcribe(audio_path='/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot/media_folder/voice_13.wav')
    print(result)
    assert isinstance(result, str)

# if __name__ == '__main__':
#     test_speech_to_text()