from envparse import env
from vkbottle import Bot

from modules import modules_list
from db.tortoise_init import db_init, db_shutdown
from middlewares import registration

env.read_envfile(".env")
bot = Bot(env.str("BOT_TOKEN"))


for bp in modules_list:
    bp.load(bot)


bot.labeler.message_view.register_middleware(
    registration.RegistrationMiddleware)


if __name__ == "__main__":
    bot.loop_wrapper.on_startup.append(db_init())
    bot.loop_wrapper.on_shutdown.append(db_shutdown())
    bot.loop_wrapper.auto_reload = True
    bot.run_forever()
