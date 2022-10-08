from loguru import logger
from tortoise.exceptions import DoesNotExist
from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from src.blueprints.chat_invite import init_chat
from src.db.models import Chat, User


class StatisticMiddleware(BaseMiddleware[Message]):
    @logger.catch()
    async def pre(self):
        if not await self._init():
            await init_chat(self.event.peer_id)
        await self._init()
        self.send({"chat": self.chat, "user": self.user})

    @logger.catch()
    async def _init(self):
        try:
            self.chat = await Chat.get(id=self.event.peer_id)
            self.user = await User.get(chat=self.chat, uid=self.event.from_id)
            return True
        except DoesNotExist:
            return False

    @logger.catch()
    async def post(self):
        self.chat.messages_count += 1
        await self.chat.save(update_fields=("messages_count",))
        self.user.messages_count += 1
        await self.user.save(update_fields=("messages_count",))
