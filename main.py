from csv import DictReader

import aiogram
from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
import dotenv
import logging
from typing import Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO)
BOT_API_KEY = dotenv.get_key(dotenv_path='.env', key_to_get='BOT_API_KEY')
bot = Bot(token=BOT_API_KEY)

dp = Dispatcher()

hash_map: Dict[str, str] = {}

"""
                USERID
                |      \
                ^       ^
          MEDIA_FOLDER  PREANSWER
"""

#Importing handlers
from message_templates.commands import rt as commands_dp
from content_handler.img_handler import ImgHandler
from content_handler.voice_handler import VoiceHandler

img_handler = ImgHandler(bot=bot)
voice_handler = VoiceHandler(bot=bot)

dp.include_routers(commands_dp, img_handler.rt, voice_handler.rt)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())