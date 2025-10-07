import openai
from openai import OpenAI

class SpeechToText:
    def __init__(self, client: OpenAI):
        self.client = client

    def transcribe(self, audio_path: str) -> str:
        with open(audio_path, "rb") as audio_file:
            transcriptions = self.client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=audio_file,
                response_format="text"
            )
            return transcriptions