from envparse import env
from tortoise import Tortoise

env.read_envfile(".env")


TORTOISE_ORM = {
    "connections": {"default": ("postgres://"
                    f"{env.str('POSTGRES_USER')}:"
                    f"{env.str('POSTGRES_USER_PASSWORD')}@"
                    f"{env.str('POSTGRES_HOST')}:{env.str('POSTGRES_PORT')}"
                    f"/{env.str('POSTGRES_DB_NAME')}"),
                    "sqlite_DEBUG": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["modules.new_models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def db_init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def db_shutdown():
    await Tortoise.close_connections()
