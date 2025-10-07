from aiogram import types, Bot, Router
from aiogram.enums import ContentType

class VoiceHandler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.rt = Router()

        @self.rt.message(lambda message: message.content_type == ContentType.VOICE)
        async def handle_voice(message: types.Message):
            print('Voice message received')
            await self.bot.download(file=message.voice.file_id, destination=f'/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot/media_folder/voice_{message.message_id}.wav')