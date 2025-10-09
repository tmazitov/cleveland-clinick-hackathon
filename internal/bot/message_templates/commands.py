from aiogram import Dispatcher, Bot, types, Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup
from internal.services.cache.redis_manager import RedisManager
rt = Router()

EMERGENCY_PHONE = "+999"
EMERGENCY_LINK = f"tel:{EMERGENCY_PHONE}"

class CommandsManager:
    def __init__(self, redis_client: RedisManager):
        self.redis_client = redis_client
        self.rt = rt

        @self.rt.message(Command('start'))
        async def start(message: types.Message) -> None:
            self.redis_client.delete_user_if_exists(message.from_user.id)

            kb = InlineKeyboardBuilder()
            kb.add(
                InlineKeyboardButton(text='Check symptoms', callback_data='check_symptoms'),
                InlineKeyboardButton(text='Request a doctor', callback_data='request_doctor'),
            )

            text = (
                "👋 Hello! I’m <b>Cleveland Bot</b>.\n\n"
                "I can help you:\n"
                "• check your symptoms and suggest next steps\n"
                "• find relevant doctors at Cleveland Clinic Abu Dhabi\n\n"
                "If this is an <b>emergency</b>, use /emergency immediately.\n"
                f"Or call: <b>{EMERGENCY_PHONE}</b>\n\n"
                "Type your symptoms in one message (voice notes are OK)."
            )
            await message.answer(text, reply_markup=kb.as_markup(), parse_mode="HTML")

        @self.rt.message(Command('help'))
        async def help_cmd(message: types.Message) -> None:
            help_text = (
                "<b>How I can help</b>\n"
                "• Describe your symptoms in one message (you can also send a voice note).\n"
                "• I’ll ask a few follow-up questions and share guidance.\n"
                "• I can also show doctor profiles that match your case.\n\n"
                "<b>Commands</b>\n"
                "• /start – restart the bot\n"
                "• /help – this help\n"
                "• /info – about the bot & privacy\n"
                "• /emergency – urgent help info\n\n"
                "<b>Tips</b>\n"
                "• Include duration, severity, triggers, and any meds taken.\n"
                "• If sending voice, speak clearly in a quiet place.\n"
                "• You can answer follow-up questions with the buttons."
            )
            await message.answer(help_text, parse_mode="HTML")

        @self.rt.message(Command('info'))
        async def info_cmd(message: types.Message) -> None:
            info_text = (
                "<b>About this bot</b>\n"
                "This assistant helps triage symptoms and surface relevant doctors at "
                "Cleveland Clinic Abu Dhabi. It’s for information only and <b>not a substitute for professional medical advice</b>.\n\n"
                "<b>What I do</b>\n"
                "• Collect your symptom description (text or voice)\n"
                "• Ask targeted questions to clarify your situation\n"
                "• Provide general guidance and when to seek care\n"
                "• Show doctor profiles related to your symptoms\n\n"
                "<b>Limitations</b>\n"
                "• No diagnosis or prescriptions\n"
                "• May make mistakes—use your judgment\n"
                "• If symptoms worsen or you feel unsafe, use /emergency\n\n"
                "<b>Privacy</b>\n"
                "Your messages are processed to generate guidance and match doctors. "
                "Avoid sharing IDs, card numbers, or other sensitive personal data.\n\n"
                "<b>Support</b>\n"
                f"For urgent matters, call <b>{EMERGENCY_PHONE}</b> or use /emergency."
            )
            await message.answer(info_text, parse_mode="HTML")

        @self.rt.message(Command('emergency'))
        async def emergency_cmd(message: types.Message) -> None:
            kb = InlineKeyboardBuilder()
            kb.add(InlineKeyboardButton(text=f"📞 Call {EMERGENCY_PHONE}", callback_data="lalalal"))
            kb.add(InlineKeyboardButton(text="📍 Share location", callback_data="share_location"))
            kb.adjust(1)

            emergency_text = (
                "🚨 <b>Emergency guidance</b>\n"
                "If you have severe chest pain, difficulty breathing, signs of stroke, "
                "severe bleeding, a serious injury, or sudden vision loss, <b>seek emergency care now</b>.\n\n"
                f"• Call emergency: <b>+999</b>\n"
                "• If you’re alone, try to notify someone nearby\n"
                "• Keep your phone on and location services enabled\n\n"
                "<b>Eye emergencies</b> (chemicals, high-speed impact, severe pain, sudden vision changes):\n"
                "• Rinse with clean water if chemical exposure\n"
                "• Do not rub or patch the eye\n"
                "• Remove contact lenses if possible\n"
                "• Go to the nearest emergency department immediately"
            )
            await message.answer(emergency_text, reply_markup=kb.as_markup(), parse_mode="HTML")
