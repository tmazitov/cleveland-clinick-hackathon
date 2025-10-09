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
import html
from aiogram.enums import ParseMode
from internal.bot.waiting import WaitDots
from internal.bot.message_templates.post_handler import PostHandler
import asyncio

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

        TG_LIMIT = 4096

        def format_assessment_en(data: dict) -> str:
            diagnoses = data.get("diagnoses") or []
            recommendations = (data.get("recommendations") or "").strip()

            parts = []
            if diagnoses:
                diag_lines = "\n".join(f"• {html.escape(d)}" for d in diagnoses)
                parts.append(f"<b>Possible causes</b>:\n{diag_lines}")

            if recommendations:
                parts.append(f"<b>Recommendations</b>:\n{html.escape(recommendations)}")

            return "\n\n".join(parts).strip()

        def split_by_limit(text: str, limit: int = TG_LIMIT):
            if len(text) <= limit:
                return [text]
            chunks, cur = [], []
            cur_len = 0
            for line in text.split("\n"):
                add = (line + "\n")
                if cur_len + len(add) > limit:
                    chunks.append("".join(cur).rstrip("\n"))
                    cur, cur_len = [add], len(add)
                else:
                    cur.append(add);
                    cur_len += len(add)
            if cur:
                chunks.append("".join(cur).rstrip("\n"))
            return chunks

        async def send_assessment_en(bot, chat_id: int, parsed: dict):
            text = format_assessment_en(parsed)
            for chunk in split_by_limit(text):
                await bot.send_message(
                    chat_id=chat_id,
                    text=chunk,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )

        @self.rt.callback_query(F.data.endswith(":yes"))
        async def add_symptoms(callback_query: types.CallbackQuery, state: FSMContext) -> None:
            await callback_query.answer()

            data = await state.get_data()
            questions_list = data["questions"]
            current_question = int(data["current_question"]) + 1

            if current_question >= len(questions_list):
                async with WaitDots(self.bot, callback_query.from_user.id, "Wait please"):
                    def _compute():
                        user_answers = self.redis_client.get_user_symptoms(user_id=callback_query.from_user.id)
                        ua_json = answers_to_json(user_answers)
                        req = Requester(client=self.openai_client)
                        parser = Parser()
                        parsed_local = parser.parse(req.send(user_request=ua_json))
                        print(parsed_local)
                        return parsed_local

                    parsed = await asyncio.to_thread(_compute)

                    await send_assessment_en(self.bot, callback_query.from_user.id, parsed)
                    doctors: list[Doctor] = await self.res_inst.find_doctors(
                        parsed["diagnoses"], user_id=callback_query.from_user.id
                    )

                    post_handler = PostHandler(bot=self.bot)
                    await post_handler.handle_post_symptoms(doctors=doctors, user_id=callback_query.from_user.id)
                return

            self.redis_client.set_user_symptoms(
                user_id=callback_query.from_user.id,
                symptom_key=questions_list[current_question],
                user_choose="yes"
            )
            await state.update_data(current_question=str(current_question))
            await callback_query.message.edit_text(
                text=f"{questions_list[current_question]}",
                reply_markup=_qa_keyboard(current_question)
            )

        @self.rt.callback_query(F.data.endswith(":no"))
        async def add_symptoms(callback_query: types.CallbackQuery, state: FSMContext) -> None:
            # data = await state.get_data()
            # questions_list = data["questions"]
            # current_question = data["current_question"]
            # current_question = int(current_question) + 1
            # if (current_question >= len(questions_list)):
            #     await callback_query.message.edit_text(text="Wait please...")
            #     return
            # self.redis_client.set_user_symptoms(user_id=callback_query.from_user.id,
            #                                     symptom_key=questions_list[current_question],
            #                                     user_choose="no")
            # await state.update_data(current_question=str(current_question))
            # await callback_query.message.edit_text(text=f"{questions_list[current_question]}",
            #                                        reply_markup=_qa_keyboard(current_question))
            await callback_query.answer()

            data = await state.get_data()
            questions_list = data["questions"]
            current_question = int(data["current_question"]) + 1

            if current_question >= len(questions_list):
                async with WaitDots(self.bot, callback_query.from_user.id, "Wait please"):
                    def _compute():
                        user_answers = self.redis_client.get_user_symptoms(user_id=callback_query.from_user.id)
                        ua_json = answers_to_json(user_answers)
                        req = Requester(client=self.openai_client)
                        parser = Parser()
                        parsed_local = parser.parse(req.send(user_request=ua_json))
                        print(parsed_local)
                        return parsed_local

                    parsed = await asyncio.to_thread(_compute)

                    await send_assessment_en(self.bot, callback_query.from_user.id, parsed)
                    doctors: list[Doctor] = await self.res_inst.find_doctors(
                        parsed["diagnoses"], user_id=callback_query.from_user.id
                    )

                    post_handler = PostHandler(bot=self.bot)
                    await post_handler.handle_post_symptoms(doctors=doctors, user_id=callback_query.from_user.id)
                return

            self.redis_client.set_user_symptoms(
                user_id=callback_query.from_user.id,
                symptom_key=questions_list[current_question],
                user_choose="no"
            )
            await state.update_data(current_question=str(current_question))
            await callback_query.message.edit_text(
                text=f"{questions_list[current_question]}",
                reply_markup=_qa_keyboard(current_question)
            )

        @self.rt.callback_query(F.data.endswith(":idk"))
        async def add_symptoms(callback_query: types.CallbackQuery, state: FSMContext) -> None:
            # data = await state.get_data()
            # questions_list = data["questions"]
            # current_question = data["current_question"]
            # current_question = int(current_question) + 1
            # if (current_question >= len(questions_list)):
            #     await callback_query.message.edit_text(text="Wait please...")
            #     return
            # self.redis_client.set_user_symptoms(user_id=callback_query.from_user.id,
            #                                     symptom_key=questions_list[current_question],
            #                                     user_choose="idk")
            # await state.update_data(current_question=str(current_question))
            # prev_message_id = data["message_id"]
            # await callback_query.message.edit_text(text=f"{questions_list[current_question]}",
            #                                        reply_markup=_qa_keyboard(current_question))
            await callback_query.answer()

            data = await state.get_data()
            questions_list = data["questions"]
            current_question = int(data["current_question"]) + 1

            if current_question >= len(questions_list):
                async with WaitDots(self.bot, callback_query.from_user.id, "Wait please"):
                    def _compute():
                        user_answers = self.redis_client.get_user_symptoms(user_id=callback_query.from_user.id)
                        ua_json = answers_to_json(user_answers)
                        req = Requester(client=self.openai_client)
                        parser = Parser()
                        parsed_local = parser.parse(req.send(user_request=ua_json))
                        print(parsed_local)
                        return parsed_local

                    parsed = await asyncio.to_thread(_compute)

                    await send_assessment_en(self.bot, callback_query.from_user.id, parsed)
                    doctors: list[Doctor] = await self.res_inst.find_doctors(
                        parsed["diagnoses"], user_id=callback_query.from_user.id
                    )

                    post_handler = PostHandler(bot=self.bot)
                    await post_handler.handle_post_symptoms(doctors=doctors, user_id=callback_query.from_user.id)
                return

            self.redis_client.set_user_symptoms(
                user_id=callback_query.from_user.id,
                symptom_key=questions_list[current_question],
                user_choose="idk"
            )
            await state.update_data(current_question=str(current_question))
            await callback_query.message.edit_text(
                text=f"{questions_list[current_question]}",
                reply_markup=_qa_keyboard(current_question)
            )