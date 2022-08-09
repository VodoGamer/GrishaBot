'''init db'''
from envparse import env
from loguru import logger
from tortoise import Tortoise

from src.settings.update_settings import update_all_settings

env.read_envfile(".env")


TORTOISE_ORM = {
    "connections": {
        "default": (
            f"postgres://{env.str('POSTGRES_USER')}:"
            f"{env.str('POSTGRES_USER_PASSWORD')}@"
            f"{env.str('POSTGRES_HOST')}:{env.str('POSTGRES_PORT')}"
            f"/{env.str('POSTGRES_DB_NAME')}"),
        "sqlite_DEBUG": "sqlite://db.sqlite3"
    },
    "apps": {
        "models": {
            "models": ["src.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def db_init():
    await Tortoise.init(config=TORTOISE_ORM)
    await update_all_settings()
    logger.info("All chat settings have been updated")


async def db_shutdown():
    await Tortoise.close_connections()
