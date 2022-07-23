import asyncio

from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from db.new_models import Chat, Setting
from db.tortoise_init import db_init, db_shutdown


class JSONSettings(BaseModel):
    id: int
    enabled: bool
    title: str
    default_value: int
    max_value: int


class BaseSettings(BaseModel):
    settings: list[JSONSettings]


default_settings = BaseSettings.parse_file(
    "src/settings/default_settings.json")


async def update_chat_settings(chat_id: int):
    for setting in default_settings.settings:
        setting_db = await Setting.get_or_create(
            {"title": setting.title,
             "value": setting.default_value,
             "max_value": setting.max_value},
            chat_id=chat_id,
            id=setting.id)

        if setting_db[0].title != setting.title:
            setting_db[0].title = setting.title

        if setting_db[0].max_value != setting.max_value:
            setting_db[0].max_value = setting.max_value

        await setting_db[0].save()


async def update_all_settings():
    await db_init()
    for chat in await Chat.all().order_by("id"):
        await update_chat_settings(chat.id)
    await db_shutdown()


if __name__ == "__main__":
    asyncio.run(update_all_settings())
