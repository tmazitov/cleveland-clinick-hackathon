import sys
sys.path.append("/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot")
from aiogram import types, Router, Bot
from internal.services.doctors_provider.doctor import Doctor
from typing import List, Dict
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
import html
from aiogram.enums import ParseMode

class PostHandler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.rt = Router()

    async def handle_post_symptoms(self, doctors: List[Doctor], user_id: int) -> None:
        if doctors is None or len(doctors) == 0:
            await self.bot.send_message(
                text="Sorry, I couldn't find any doctors for your symptoms. Please try again later or contact support.",
                chat_id=user_id
            )
            return
        prepared_text = "Based on your symptoms, here are some doctors you can consider:\n"
        await self.bot.send_message(text=prepared_text, chat_id=user_id)
        for doc in doctors:
            # doc_info = f"""
            # {doc.image}
            # 👨‍⚕️ Name: {doc.name}
            # 🩺 Specialty: {doc.role}
            # """
            caption = (
                f'<b><a href="{doc.image}">👨‍⚕️ {html.escape(doc.name)}</a></b>\n'
                f'🩺 Specialty: {html.escape(doc.role)}'
            )
            kb = InlineKeyboardBuilder()
            kb.add(InlineKeyboardButton(text="View Profile", url=doc.link))

            await self.bot.send_message(text=caption, reply_markup=kb.as_markup(), chat_id=user_id, parse_mode=ParseMode.HTML)
        return