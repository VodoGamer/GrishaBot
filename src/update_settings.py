import asyncio

from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from modules.new_models import Chat, Setting
from db.tortoise_init import db_init, db_shutdown


class JSONSettings(BaseModel):
    id: int
    enabled: bool
    title: str
    default_value: int


class BaseSettings(BaseModel):
    settings: list[JSONSettings]


default_settings = BaseSettings.parse_file("src/settings/default_settings.json")


async def update_chat_settings(chat_id: int):
    for setting in default_settings.settings:
        try:
            setting_db = await Setting.get(chat_id=chat_id, id=setting.id)
        except DoesNotExist:
            setting_db = Setting(chat_id=chat_id,
                                    id=setting.id,
                                    title=setting.title,
                                    value=setting.default_value)
            await setting_db.save()
            return

        if setting_db.title != setting.title:
            setting_db = Setting(chat_id=chat_id,
                                    id=setting.id,
                                    title=setting.title)
            await setting_db.save()


async def update_all_settings():
    await db_init()
    for chat in await Chat.all().order_by("id"):
        await update_chat_settings(chat.id)
    await db_shutdown()


if __name__ == "__main__":
    asyncio.run(update_all_settings())
