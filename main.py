from loguru import logger
from vkbottle import Bot, BaseMiddleware
from vkbottle.bot import Message
from modules import modules_list
import config


logger.add("debug.log", format="{time} | {level} | {message}", level="DEBUG")


bot = Bot(config.TOKEN)


for bp in modules_list:
    bp.load(bot)

from modules import models


class RegistrationMiddleware(BaseMiddleware[Message]):
    '''
    Мидлварь для статистики и регистрации новых пользователей и чатов
    '''
    async def post(self):
        user = models.User(self.event.peer_id, self.event.from_id)
        if user.check():
            user.add_message()
        else:
            user.register()

        if str(self.event.peer_id)[0] == "2":
            chat = models.Chat(self.event.peer_id)
            chat_vk = await bot.api.messages.get_conversations_by_id(self.event.peer_id)
            owner_id = chat_vk.items[0].chat_settings.owner_id
            if chat.check():
                chat.add_message()
            else:
                chat.register(owner_id)


bot.labeler.message_view.register_middleware(RegistrationMiddleware)

bot.run_forever()
