from loguru import logger
from vkbottle import ABCAPI, BaseMiddleware
from vkbottle.bot import Message

from src.db.models import Chat, User
from src.settings.update_settings import update_chat_settings


async def get_chat_settings(api: ABCAPI, chat_id: int):
    return (await api.messages.get_conversations_by_id(
        [chat_id])).items[0].chat_settings


class RegistrationMiddleware(BaseMiddleware[Message]):
    '''
    Мидлварь для статистики и регистрации новых пользователей и чатов
    '''
    @logger.catch()
    async def pre(self):
        ...
        # logger.debug("RegistrationMiddleware Pre init")
        # # Chat
        # chat = await Chat.get_or_create(id=self.event.peer_id)

        # if chat[1]:  # Если чат был зарегистрирован при вызове
        #     chat_vk = await get_chat_settings(self.event.ctx_api,
        #                                       self.event.peer_id)

        #     if chat_vk is None:
        #         logger.error("Запрос данных о чате вернул NONE!")
        #     else:
        #         chat[0].owner_id = chat_vk.owner_id
        #         await chat[0].save()

        #         if chat_vk.admin_ids is None:
        #             logger.error("В чате нет ни одного админа!")
        #         else:
        #             # Регистрируем админов беседы
        #             for admin_id in chat_vk.admin_ids:
        #                 if admin_id > 0:
        #                     await User.get_or_create(
        #                         {"messages_count": 0},
        #                         id=admin_id,
        #                         chat_id=chat[0].id,
        #                         is_admin=1)

        #         # Регистрируем овнера беседы как админа
        #         await User.get_or_create(
        #             {"messages_count": 0},
        #             id=chat_vk.owner_id,
        #             chat_id=chat[0].id,
        #             is_admin=1)

        #     # Регистрируем нашу группу как пользователя
        #     await User.create(
        #         id=-(await self.event.ctx_api.groups.get_by_id())[0].id,
        #         chat_id=chat[0].id
        #     )

        #     await update_chat_settings(chat[0].id)

        # # User
        # user = await User.get_or_create(id=self.event.from_id,
        #                                 chat_id=self.event.peer_id)

        # self.chat = chat[0]
        # self.user = user[0]

        # # Отправка данных о чате и пользователе в хендлеры
        # self.send({"chat": chat[0]})
        # self.send({"user": user[0]})
        # logger.debug("RegistrationMiddleware Pre successfully completed")

    # @logger.catch()
    # async def post(self):
        # logger.debug("RegistrationMiddleware Post init")
        # self.chat.messages_count += 1
        # await self.chat.save(update_fields=("messages_count",))

        # self.user.messages_count += 1
        # await self.user.save(update_fields=("messages_count",))
        # logger.debug("RegistrationMiddleware Post successfully completed")
