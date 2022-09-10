from loguru import logger
from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from src.db.models import Chat, User


class StatisticMiddleware(BaseMiddleware[Message]):
    @logger.catch()
    async def pre(self):
        self.chat = await Chat.get(id=self.event.peer_id)
        self.user = await User.get(chat=self.chat, id=self.event.from_id)
        self.send({"chat": self.chat, "user": self.user})

    @logger.catch()
    async def post(self):
        self.chat.messages_count += 1
        await self.chat.save(update_fields=("messages_count",))
        self.user.messages_count += 1
        await self.user.save(update_fields=("messages_count",))
