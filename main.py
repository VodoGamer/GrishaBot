from vkbottle import Bot, BaseMiddleware
from vkbottle.bot import Message
from modules import modules_list, models
import config


bot = Bot(config.TOKEN)


for bp in modules_list:
    bp.load(bot)


class RegistrationMiddleware(BaseMiddleware[Message]):
    '''
    Мидлварь для статистики и регистрации новых пользователей и чатов
    '''
    async def post(self):
        user = models.User(self.event.peer_id, self.event.from_id)
        user.add_message()

        if len(str(self.event.peer_id)) == 10:
            chat = models.Chat(self.event.peer_id)
            settings = models.Settings(self.event.peer_id)
            settings.update()
            if chat.check():
                chat.add_message()
            else:
                chat_vk = await bot.api.messages.get_conversations_by_id(
                    self.event.peer_id)
                owner_id = chat_vk.items[0].chat_settings.owner_id
                chat.register(owner_id)


bot.labeler.message_view.register_middleware(RegistrationMiddleware)
bot.run_forever()
