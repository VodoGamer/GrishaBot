'''building a bot'''
from vkbottle import Bot

from src.blueprints import modules_list
from src.config.db import db_init, db_shutdown
from src.config.env import VK_TOKEN
from src.middleware.statistic import StatisticMiddleware
from src.settings.update_settings import update_all_settings
from src.repository import account


def init_middlewares(bot: Bot) -> None:
    bot.labeler.message_view.register_middleware(StatisticMiddleware)


def init_loop_wrappers(bot: Bot) -> None:
    bot.loop_wrapper.on_startup.append(db_init())
    bot.loop_wrapper.on_startup.append(update_all_settings())
    bot.loop_wrapper.on_shutdown.append(db_shutdown())


def init_blueprints(bot: Bot):
    account.bp.load(bot)
    for bp in modules_list:
        bp.load(bot)


def init_bot() -> Bot:
    bot = Bot(VK_TOKEN)
    init_middlewares(bot)
    init_loop_wrappers(bot)
    init_blueprints(bot)
    return bot
