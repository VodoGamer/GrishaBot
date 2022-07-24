from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from bot_init import bot
from db.new_models import Chat, User
from update_settings import update_chat_settings


class RegistrationMiddleware(BaseMiddleware[Message]):
    '''
    Мидлварь для статистики и регистрации новых пользователей и чатов
    '''
    async def pre(self):
        # Chat
        self.chat = await Chat.get_or_create(id=self.event.peer_id)

        if self.chat[1]:
            # Получаем информацию о беседе
            chat_vk = (await bot.api.messages.get_conversations_by_id(
                [self.event.peer_id])).items[0].chat_settings

            self.chat[0].owner_id = chat_vk.owner_id  # type: ignore
            await self.chat[0].save()

            # Регистрируем админов беседы
            for admin_id in chat_vk.admin_ids:  # type: ignore
                if admin_id > 0:
                    await User.get_or_create(
                        {"messages_count": 0},
                        id=admin_id,
                        chat_id=self.chat[0].id,
                        is_admin=1)
            # Регистрируем овнера беседы как админа
            await User.get_or_create(
                {"messages_count": 0},
                id=chat_vk.owner_id,  # type: ignore
                chat_id=self.chat[0].id,
                is_admin=1)

            # Регистрируем группу как пользователя
            await User.create(id=-(await bot.api.groups.get_by_id())[0].id,
                              chat_id=self.chat[0].id)

            await update_chat_settings(self.chat[0].id)

        self.send({"chat": self.chat[0]})

        # User
        self.user = await User.get_or_create(id=self.event.from_id,
                                             chat_id=self.event.peer_id)

        self.send({"user": self.user[0]})

    async def post(self):
        self.chat[0].messages_count += 1
        await self.chat[0].save()
        self.user[0].messages_count += 1
        await self.user[0].save()
