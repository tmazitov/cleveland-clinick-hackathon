import sys, aiogram
from aiogram.fsm.middleware import FSMContext
from aiogram import Router, Bot, types
from internal.bot.fsm_machine.user_cls import UserState
from internal.services.cache.redis_manager import RedisManager
from internal.parser.parser_manager import Parser
from internal.requester.requester import Requester
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
import openai

class FSMHandler:
    def __init__(self, redis_client: RedisManager, openai_client: openai.OpenAI):
        self.redis_client = redis_client
        self.openai_client = openai_client
        self.rt = Router()

        def _qa_keyboard(symptom: str) -> types.InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()
            kb.button(text="yes", callback_data=f"{symptom}:yes")
            kb.button(text="no", callback_data=f"{symptom}:no")
            kb.button(text="IDK", callback_data=f"{symptom}:idk")
            kb.adjust(3)
            return kb.as_markup()

        @self.rt.message(UserState.symptoms)
        async def handle_explained_sympthom(message: types.Message, state: FSMContext) -> None:
            parser = Parser()
            requester = Requester(client=self.openai_client)
            text = "Okay!\nLet me check your situation and ask couple of additional questions..."
            self.redis_client.set_user_explained(user_id=message.from_user.id, explained=message.text)
            await message.answer(text=text)
            await state.clear()
            questions = parser.parse(requester.send(user_request=message.text))
            questions_list = questions.get("questions", [])
            if not questions_list:
                await message.answer("Need more information from you!")
                return
            await state.update_data(questions=questions_list)
            await state.update_data(current_question=str(0))
            sent = await message.answer(f"{questions_list[0]}", reply_markup=_qa_keyboard(0))
            await state.update_data(message_id=sent.message_id)
            # for question in questions["questions"]:
            #     bt_yes = InlineKeyboardButton(text="yes", callback_data=f"{x}_yes")
            #     bt_no = InlineKeyboardButton(text="no", callback_data=f"{x}_no")
            #     bt_idk = InlineKeyboardButton(text="idk", callback_data=f"{x}_idk")
            #     kb = InlineKeyboardBuilder()
            #     kb.add(bt_yes, bt_no, bt_idk)
            #     await message.answer(text=question, reply_markup=kb.as_markup())
