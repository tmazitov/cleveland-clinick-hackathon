from aiogram import types, Bot, Router
from aiogram.enums import ContentType

from settings import MEDIA

class VoiceHandler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.rt = Router()

        # @self.rt.message(lambda message: message.content_type == ContentType.VOICE)
        # async def handle_voice(message: types.Message):
        #     print('Voice message received')
        #     await self.bot.download(file=message.voice.file_id, destination=f'{MEDIA}/voice_{message.message_id}.wav')