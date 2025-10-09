import sys, aiogram
from aiogram.fsm.middleware import FSMContext
from aiogram import Router, Bot, types
from internal.bot.fsm_machine.user_cls import UserState
from internal.services.cache.redis_manager import RedisManager
from internal.parser.parser_manager import Parser
from internal.requester.requester import Requester
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
import openai
from aiogram import F
from internal.services.sp_2_tx.sp_2_tx import *
import tempfile
from aiogram.types import InlineKeyboardMarkup
from internal.bot.waiting import WaitDots


class FSMHandler:
    def __init__(self, redis_client: RedisManager, openai_client: openai.OpenAI, bot: Bot):
        self.redis_client = redis_client
        self.openai_client = openai_client
        self.bot = bot
        self.rt = Router()

        def _qa_keyboard(symptom: str) -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()
            kb.button(text="yes", callback_data=f"{symptom}:yes")
            kb.button(text="no", callback_data=f"{symptom}:no")
            kb.button(text="IDK", callback_data=f"{symptom}:idk")
            kb.adjust(3)
            return kb.as_markup()

        FFMPEG_BIN = "ffmpeg"

        import os, asyncio
        from pathlib import Path
        from aiogram import types, Bot
        from openai import OpenAI

        FFMPEG_BIN = "ffmpeg"

        async def _run_ffmpeg_to_wav(src: Path, dst: Path) -> None:
            if not src.exists() or src.stat().st_size == 0:
                raise RuntimeError(f"[FFMPEG] source missing/empty: {src}")
            dst.parent.mkdir(parents=True, exist_ok=True)

            proc = await asyncio.create_subprocess_exec(
                FFMPEG_BIN, "-y", "-i", str(src), "-ar", "16000", "-ac", "1", str(dst),
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            out, err = await proc.communicate()
            if proc.returncode != 0:
                raise RuntimeError(f"[FFMPEG] failed ({proc.returncode}): {err.decode(errors='ignore')[:400]}")
            if not dst.exists() or dst.stat().st_size == 0:
                raise RuntimeError(f"[FFMPEG] dst wav missing/empty: {dst}")
            print(f"[FFMPEG] OK: {src.name} -> {dst.name} ({dst.stat().st_size} bytes)")

        async def _download_media_to(bot: Bot, message: types.Message, dst: Path) -> None:
            if message.voice:
                await bot.download(message.voice, destination=dst)
                print(f"[DL] voice -> {dst} ({dst.stat().st_size} bytes)")
            elif message.audio:
                await bot.download(message.audio, destination=dst)
                print(f"[DL] audio -> {dst} ({dst.stat().st_size} bytes)")
            elif message.video_note:
                await bot.download(message.video_note, destination=dst)
                print(f"[DL] video_note -> {dst} ({dst.stat().st_size} bytes)")
            else:
                raise ValueError("[DL] No media to download")
            if dst.stat().st_size == 0:
                raise RuntimeError("[DL] downloaded file is empty")


        @self.rt.message(
            UserState.symptoms,
            F.text | F.voice | F.audio | F.video_note
        )
        async def handle_explained_symptom(message: types.Message, state: FSMContext, bot: Bot) -> None:
            # запуск анимации: это и будет «Okay, got you!...» с бегущими точками
            async with WaitDots(self.bot, message.chat.id,
                                "Okay, got you!\nLet me figure out your case and ask couple of additional questions"):
                user_text = None

                # 1) получаем текст от пользователя
                if message.text:
                    user_text = message.text.strip()
                else:
                    stt = SpeechToText(client=self.openai_client)
                    with tempfile.TemporaryDirectory() as td:
                        td = Path(td)
                        src = td / "input.bin"
                        wav = td / "input.wav"

                        await _download_media_to(bot, message, src)
                        await _run_ffmpeg_to_wav(src, wav)

                        # НЕ вызываем _do_stt() напрямую — только через to_thread
                        user_text = await asyncio.to_thread(stt.transcribe, str(wav))

                if not user_text:
                    # выйдем из контекста (анимация остановится) и ответим ошибкой
                    await message.answer("I couldn't get your message. Please try again.")
                    return

                # 2) сохраняем описание и получаем вопросы от модели (синхронное — в to_thread)
                self.redis_client.set_user_explained(user_id=message.from_user.id, explained=user_text)

                parser = Parser()
                requester = Requester(client=self.openai_client)

                def _ask_model():
                    return parser.parse(requester.send(user_request=user_text))

                result = await asyncio.to_thread(_ask_model)
                questions_list = result.get("questions", []) or []

                await state.clear()

                if not questions_list:
                    await message.answer("Need more information from you!")
                    return

                await state.update_data(questions=questions_list, current_question="0")
                sent = await message.answer(questions_list[0], reply_markup=_qa_keyboard(0))
                await state.update_data(message_id=sent.message_id)




        # async def handle_explained_symptom(message: types.Message, state: FSMContext, bot: Bot) -> None:
        #     await message.answer(
        #         "Okay, got you!\nLet me figure out your case and ask couple of additional questions...")
        #
        #     user_text = None
        #     if message.text:
        #         user_text = message.text.strip()
        #     else:
        #         stt = SpeechToText(client=self.openai_client)
        #         with tempfile.TemporaryDirectory() as td:
        #             td = Path(td)
        #             src = td / "input.bin"
        #             wav = td / "input.wav"
        #             await _download_media_to(bot, message, src)
        #             await _run_ffmpeg_to_wav(src, wav)
        #
        #             def _do_stt():
        #                 return stt.transcribe(str(wav))
        #             print(_do_stt())
        #             user_text = await asyncio.to_thread(_do_stt)
        #
        #     if not user_text:
        #         await message.answer("I couldn't get your message. Please try again.")
        #         return
        #
        #     self.redis_client.set_user_explained(user_id=message.from_user.id, explained=user_text)
        #
        #     parser = Parser()
        #     requester = Requester(client=self.openai_client)
        #
        #     def _ask_model():
        #         return parser.parse(requester.send(user_request=user_text))
        #
        #     result = await asyncio.to_thread(_ask_model)
        #     questions_list = result.get("questions", []) or []
        #
        #     await state.clear()
        #
        #     if not questions_list:
        #         await message.answer("Need more information from you!")
        #         return
        #
        #     await state.update_data(questions=questions_list, current_question="0")
        #     sent = await message.answer(questions_list[0], reply_markup=_qa_keyboard(0))
        #     await state.update_data(message_id=sent.message_id)