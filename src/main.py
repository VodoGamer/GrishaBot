from bot_init import bot
from db.tortoise_init import db_init, db_shutdown
from middlewares.registration import RegistrationMiddleware
from modules import modules_list
from repository import account

account.bp.load(bot)
for bp in modules_list:
    bp.load(bot)


if __name__ == "__main__":
    bot.labeler.message_view.register_middleware(RegistrationMiddleware)
    bot.loop_wrapper.on_startup.append(db_init())
    bot.loop_wrapper.on_shutdown.append(db_shutdown())
    bot.loop_wrapper.auto_reload = True
    bot.run_forever()
