from envparse import env
from vkbottle import BaseMiddleware, Bot
from vkbottle.bot import Message

from modules import models, modules_list


env.read_envfile(".env")
bot = Bot(env.str("BOT_TOKEN"))


for bp in modules_list:
    bp.load(bot)


class RegistrationMiddleware(BaseMiddleware[Message]):
    '''
    Мидлварь для статистики и регистрации новых пользователей и чатов
    '''
    async def post(self):
        user = models.User(self.event.peer_id, self.event.from_id)
        await user.init()
        await user.add_message()

        if len(str(self.event.peer_id)) == 10:
            chat = models.Chat(self.event.peer_id)
            await chat.init()
            settings = models.Settings(self.event.peer_id)
            await settings.update()
            if await chat.check():
                await chat.add_message()
            else:
                chat_vk = await bot.api.messages.get_conversations_by_id(
                    self.event.peer_id)
                owner_id = chat_vk.items[0].chat_settings.owner_id
                await chat.register(owner_id)


bot.labeler.message_view.register_middleware(RegistrationMiddleware)
bot.run_forever()
