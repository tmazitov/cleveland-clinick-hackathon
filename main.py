from asyncio import run
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from typing import Dict, Any, List, Optional

from settings import BOT_API_KEY
from internal.bot.handlers.img_handler import ImgHandler
from internal.bot.handlers.voice_handler import VoiceHandler
from internal.bot.message_templates.commands import rt as commands_dp


"""
                USERID
                |      \
                ^       ^
          MEDIA_FOLDER  PREANSWER
"""

#Importing handlers

async def main() -> None:
    bot = Bot(token=BOT_API_KEY)

    dp = Dispatcher()

    hash_map: Dict[str, str] = {}

    img_handler = ImgHandler(bot=bot)
    voice_handler = VoiceHandler(bot=bot)

    dp.include_routers(commands_dp, img_handler.rt, voice_handler.rt)
    await dp.start_polling(bot)

if __name__ == '__main__':
    run(main())