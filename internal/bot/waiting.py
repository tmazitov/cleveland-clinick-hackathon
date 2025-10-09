import asyncio
from aiogram import Bot

class WaitDots:
    def __init__(self, bot: Bot, chat_id: int, base_text: str = "Wait please"):
        self.bot = bot
        self.chat_id = chat_id
        self.base_text = base_text
        self._stop = asyncio.Event()
        self._task = None
        self._msg = None

    async def __aenter__(self):
        self._msg = await self.bot.send_message(self.chat_id, f"{self.base_text}.")
        self._task = asyncio.create_task(self._loop())
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self._stop.set()
        if self._task:
            try:
                await self._task
            except Exception:
                pass
        try:
            await self.bot.edit_message_text(
                chat_id=self.chat_id,
                message_id=self._msg.message_id,
                text="Done ✅"
            )
        except Exception:
            pass

    async def _loop(self):
        dots = [".", "..", "..."]
        i = 0
        while not self._stop.is_set():
            i = (i + 1) % 3
            try:
                await self.bot.edit_message_text(
                    chat_id=self.chat_id,
                    message_id=self._msg.message_id,
                    text=f"{self.base_text}{dots[i]}"
                )
            except Exception:
                pass
            await asyncio.sleep(0.7)