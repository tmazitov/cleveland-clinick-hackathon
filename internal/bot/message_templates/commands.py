from aiogram import Dispatcher, Bot, types, Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup
from internal.services.cache.redis_manager import RedisManager
rt = Router()
class CommandsManager:
    def __init__(self, redis_client: RedisManager):
        self.redis_client = redis_client
        self.rt = rt

        @self.rt.message(Command('start'))
        async def start(message: types.Message) -> None:
            self.redis_client.delete_user_if_exists(message.from_user.id)
            kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
            bt_check_symptomps: InlineKeyboardButton = InlineKeyboardButton(text='Check symptoms', callback_data='check_symptoms')
            bt_request_a_doctor: InlineKeyboardButton = InlineKeyboardButton(text='Request a docktor', callback_data='request_doctor')
            kb.add(bt_check_symptomps, bt_request_a_doctor)
            await message.answer("Hello! I'm Cleavlend Bot. How can I assist you today? If u need emergency help - click here /emergency\n"
                                 "Or call on this number: +971000000000", reply_markup=kb.as_markup())

        @self.rt.message(Command('help'))
        async def help(message: types.Message) -> None:
            help_text = ""
            await message.answer(help_text)

        @self.rt.message(Command('info'))
        async def info(message: types.Message) -> None:
            info_text = ""
            await message.answer(info_text)

        @self.rt.message(Command('emergency'))
        async def emergency(message: types.Message) -> None:
            emergency_text = ""
            await message.anwer(emergency_text)
