'''parse .env variables'''
from envparse import env


env.read_envfile(".env")
VK_TOKEN = env.str('BOT_TOKEN')
DB_CONNECT = env.str('DB_CONNECT')
