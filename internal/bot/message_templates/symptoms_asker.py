import sys

import openai

from internal.services.doctors_provider.doctor import Doctor

# from internal.services.doctors_provider.doctors_provider import DoctorsProvider

sys.path.append('/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot')
from internal.requester.requester import Requester
from internal.parser.parser_manager import Parser
from aiogram import Bot, Router, types, F
from aiogram.fsm.middleware import FSMContext
from aiogram.fsm.state import State
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from internal.bot.fsm_machine.user_cls import UserState
from internal.services.cache.redis_manager import RedisManager
from internal.requester.requester import Requester
from internal.result import Result

class SymptomsAsker:
    def __init__(self, redis_client: RedisManager, bot: Bot, openai_client: openai.OpenAI, res_inst: Result):
        self.redis_client = redis_client
        self.rt = Router()
        self.bot = bot
        self.openai_client = openai_client
        self.res_inst = res_inst


        import json

        def answers_to_json(user_answers: dict) -> str:
            def dec(x): return x.decode("utf-8") if isinstance(x, (bytes, bytearray)) else x

            ua = {dec(k): dec(v) for k, v in user_answers.items()}
            return json.dumps(ua, ensure_ascii=False, separators=(',', ':'))

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
                user_answers = self.redis_client.get_user_symptoms(user_id=callback_query.from_user.id)
                requester = Requester(client=self.openai_client)
                user_answers = answers_to_json(user_answers)
                last_parse = Parser()
                parsed = last_parse.parse(requester.send(user_request=user_answers))

                doctors:list[Doctor] = await self.res_inst.find_doctors(parsed["diagnoses"], user_id=callback_query.from_user.id)

                if doctors is None or len(doctors) == 0:
                    await callback_query.message.answer(text="Sorry, I couldn't find any doctors for your symptoms. Please try again later or contact support.")
                    return

                prepared_text = "Based on your symptoms, here are some doctors you can consider:\n"
                await callback_query.message.answer(text=prepared_text)

                for doc in doctors:
                    doc_info = f"""
                    {doc.image}
                    👨‍⚕️ Name: {doc.name}
                    🩺 Specialty: {doc.role}
                    """
                    await callback_query.message.answer(text=doc_info)

                    # Create a keyboard with a link button
                    kb = InlineKeyboardBuilder()
                    kb.add(InlineKeyboardButton(text="View Profile", url=doc.link))


                    await callback_query.message.answer(text=doc_info, reply_markup=kb.as_markup())
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