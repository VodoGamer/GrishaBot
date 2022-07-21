from tortoise.exceptions import DoesNotExist
from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from modules.new_models import Chat, User
from update_settings import update_chat_settings


class RegistrationMiddleware(BaseMiddleware[Message]):
    '''
    Мидлварь для статистики и регистрации новых пользователей и чатов
    '''
    async def pre(self):
        chat_filter = Chat.filter(id=self.event.peer_id)
        try:
            chat = await Chat.get(id=self.event.peer_id)
        except DoesNotExist:
            chat = Chat(id=self.event.peer_id,
                        owner_id=self.event.from_id)
            await chat.save()
            chat = await chat.get()
            await update_chat_settings(chat.id)

        self.send({"chat": chat})
        self.send({"chat_filter": chat_filter})
        self.chat = chat
        self.chat_filter = chat_filter

        user_filter = User.filter(chat_id=self.event.peer_id,
                                  id=self.event.from_id)
        try:
            user = await User.get(chat_id=self.event.peer_id,
                                  id=self.event.from_id)
        except DoesNotExist:
            user = User(chat_id=self.event.peer_id,
                        id=self.event.from_id)
            await user.save()
            user = await user.get()
        self.send({"user": user})
        self.send({"user_filter": user_filter})
        self.user = user
        self.user_filter = user_filter

    async def post(self):
        await self.chat_filter.update(messages_count=self.chat.messages_count + 1)
        await self.user_filter.update(messages_count=self.user.messages_count + 1)
