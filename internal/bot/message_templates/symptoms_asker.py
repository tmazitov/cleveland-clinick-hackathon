import sys
sys.path.append('/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot')
from internal.requester.requester import Requester
from internal.parser.parser_manager import Parser
from aiogram import Bot, Router, types, F
from aiogram.fsm.middleware import FSMContext
from aiogram.fsm.state import State
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from internal.bot.fsm_machine.user_cls import UserState
from internal.services.cache.redis_manager import RedisManager

class SymptomsAsker:
    def __init__(self, redis_client: RedisManager, bot: Bot):
        self.redis_client = redis_client
        self.rt = Router()
        self.bot = bot

        @self.rt.callback_query(F.data == 'check_symptoms')
        async def ask_symptoms(callback_query: types.CallbackQuery, state: FSMContext) -> None:
            # kb = InlineKeyboardBuilder()
            # bt = InlineKeyboardButton(text="Ask for symptoms", callback_data='ask_symptoms')
            # kb.add(bt)
            text = "Explain your symptoms below in one message, you can make voice message!"
            await state.set_state(UserState.symptoms)
            await state.update_data(user_id=callback_query.from_user.id)
            await callback_query.message.answer(text=text)

        @self.rt.callback_query(F.data == 'ask_symptoms')
        async def ask_symptoms(callback_query: types.CallbackQuery) -> None:
            kb = InlineKeyboardBuilder()
            bt_yes = InlineKeyboardButton(text="Yes", callback_data='yes_symptom')
            bt_no = InlineKeyboardButton(text="No", callback_data='no_symptom')
            bt_idk = InlineKeyboardButton(text="I don't know", callback_data='idk_symptom')
            kb.add(bt_yes)
            kb.add(bt_no)
            kb.add(bt_idk)
            text = "Explain your symptoms"


        def _qa_keyboard(symptom: int) -> types.InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()
            kb.button(text="yes", callback_data=f"{symptom}:yes")
            kb.button(text="no", callback_data=f"{symptom}:no")
            kb.button(text="IDK", callback_data=f"{symptom}:idk")
            kb.adjust(3)
            return kb.as_markup()

        @self.rt.callback_query(F.data.endswith(":yes"))
        async def add_symptoms(callback_query: types.CallbackQuery, state: FSMContext) -> None:
            data = await state.get_data()
            questions_list = data["questions"]
            current_question = data["current_question"]
            current_question = int(current_question) + 1
            if (current_question >= len(questions_list)):
                await callback_query.message.edit_text(text="Wait please...")
                return
            self.redis_client.set_user_symptoms(user_id=callback_query.from_user.id, symptom_key=questions_list[current_question],
                                                user_choose="yes")
            await state.update_data(current_question=str(current_question))
            prev_message_id = data["message_id"]
            await callback_query.message.edit_text(text=f"{questions_list[current_question]}", reply_markup=_qa_keyboard(current_question))

        @self.rt.callback_query(F.data.endswith(":no"))
        async def add_symptoms(callback_query: types.CallbackQuery, state: FSMContext) -> None:
            data = await state.get_data()
            questions_list = data["questions"]
            current_question = data["current_question"]
            current_question = int(current_question) + 1
            if (current_question >= len(questions_list)):
                await callback_query.message.edit_text(text="Wait please...")
                return
            self.redis_client.set_user_symptoms(user_id=callback_query.from_user.id,
                                                symptom_key=questions_list[current_question],
                                                user_choose="no")
            await state.update_data(current_question=str(current_question))
            prev_message_id = data["message_id"]
            await callback_query.message.edit_text(text=f"{questions_list[current_question]}",
                                                   reply_markup=_qa_keyboard(current_question))

        @self.rt.callback_query(F.data.endswith(":idk"))
        async def add_symptoms(callback_query: types.CallbackQuery, state: FSMContext) -> None:
            data = await state.get_data()
            questions_list = data["questions"]
            current_question = data["current_question"]
            current_question = int(current_question) + 1
            if (current_question >= len(questions_list)):
                await callback_query.message.edit_text(text="Wait please...")
                return
            self.redis_client.set_user_symptoms(user_id=callback_query.from_user.id,
                                                symptom_key=questions_list[current_question],
                                                user_choose="idk")
            await state.update_data(current_question=str(current_question))
            prev_message_id = data["message_id"]
            await callback_query.message.edit_text(text=f"{questions_list[current_question]}",
                                                   reply_markup=_qa_keyboard(current_question))