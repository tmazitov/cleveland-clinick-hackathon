from aiogram import Dispatcher, Bot, types, Router
from aiogram.filters import Command

rt = Router()

@rt.message(Command('start'))
async def start(message: types.Message) -> None:
    await message.answer("Hello! I'm Cleavlend Bot. How can I assist you today? If u need emergency help - click here /emergency")

@rt.message(Command('help'))
async def help(message: types.Message) -> None:
    help_text = ""
    await message.answer(help_text)

@rt.message(Command('info'))
async def info(message: types.Message) -> None:
    info_text = ""
    await message.answer(info_text)

@rt.message(Command('emergency'))
async def emergency(message: types.Message) -> None:
    emergency_text = ""
    await message.anwer(emergency_text)
