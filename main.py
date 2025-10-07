import aiogram
from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
import dotenv

BOT_API_KEY = dotenv.get_key(dotenv_path='.env', key_to_get='BOT_API_KEY')
bot = Bot(token=BOT_API_KEY)

dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message) -> None:
    await message.answer("Hello! I'm Cleavlend Bot. How can I assist you today?")



async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())