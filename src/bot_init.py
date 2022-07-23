from envparse import env
from vkbottle import Bot

env.read_envfile(".env")
bot = Bot(env.str("BOT_TOKEN"))
