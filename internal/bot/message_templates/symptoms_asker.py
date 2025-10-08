import sys
sys.path.append('/Users/iqment/Desktop/Learning/Hackethon/ClivlendChatBot')
from internal.requester.requester import Requester
from internal.parser.parser_manager import Parser
from aiogram import Bot, Router, types, F
from aiogram.fsm.middleware import FSMContext
from aiogram.fsm.state import State
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from internal.bot.fsm_machine.user_cls import UserState

rt = Router()

@rt.callback_query(F.data == 'check_symptoms')
async def ask_symptoms(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    # kb = InlineKeyboardBuilder()
    # bt = InlineKeyboardButton(text="Ask for symptoms", callback_data='ask_symptoms')
    # kb.add(bt)
    text = "Explain your symptoms below in one message, you can make voice message!"
    await state.set_state(UserState.symptoms)
    await state.update_data(user_id=callback_query.from_user.id)
    await callback_query.message.answer(text=text)

@rt.callback_query(F.data == 'ask_symptoms')
async def ask_symptoms(callback_query: types.CallbackQuery) -> None:
    kb = InlineKeyboardBuilder()
    bt_yes = InlineKeyboardButton(text="Yes", callback_data='yes_symptom')
    bt_no = InlineKeyboardButton(text="No", callback_data='no_symptom')
    bt_idk = InlineKeyboardButton(text="I don't know", callback_data='idk_symptom')
    kb.add(bt_yes)
    kb.add(bt_no)
    kb.add(bt_idk)
    text = "Explain your symptoms"
