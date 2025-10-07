from aiogram import Router, types, Bot
from aiogram.enums import ContentType



class ImgHandler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.rt = Router()

        @self.rt.message(lambda message: message.content_type == ContentType.PHOTO)
        async def handle_photo(message: types.Message):
            print('Photo received')
            await self.bot.download(file=message.photo[-1].file_id, destination=f'/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot/media_folder/test.jpg')