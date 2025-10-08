from asyncio import run

import dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from typing import Dict, Any, List, Optional

from settings import BOT_API_KEY
from settings import OPENAI_API_KEY
from internal.bot.handlers.img_handler import ImgHandler
from internal.bot.handlers.voice_handler import VoiceHandler
from internal.bot.message_templates.commands import rt as commands_rt
from internal.bot.message_templates.symptoms_asker import SymptomsAsker
from internal.bot.fsm_machine.fsm_handler import FSMHandler
from internal.services.cache.redis_manager import RedisManager
from openai import OpenAI


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

    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    redis_client: RedisManager = RedisManager()
    img_handler = ImgHandler(bot=bot)
    voice_handler = VoiceHandler(bot=bot)
    FSM_handler = FSMHandler(redis_client=redis_client, openai_client=openai_client)
    symptoms_asker = SymptomsAsker(redis_client=redis_client, bot=bot)
    dp.include_routers(commands_rt, img_handler.rt, voice_handler.rt, symptoms_asker.rt, FSM_handler.rt)
    await dp.start_polling(bot)

if __name__ == '__main__':
    run(main())