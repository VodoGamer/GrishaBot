import asyncio
from loguru import logger

from pydantic import BaseModel

from src.db.models import Chat, Setting


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

        if setting_db[1]:
            logger.info(
                f"a chat {chat_id} setting {setting.id} | {setting.title} "
                "has been added")

        if setting_db[0].title != setting.title:
            logger.info(f"a chat {chat_id} setting {setting.id} "
                        f"title has been edit to: {setting.title}")
            setting_db[0].title = setting.title

        if setting_db[0].max_value != setting.max_value:
            setting_db[0].max_value = setting.max_value

        await setting_db[0].save()


async def update_all_settings():
    for chat in await Chat.all().order_by("id"):
        await update_chat_settings(chat.id)
        logger.debug(f"settings of {chat.id} chat updated!")


if __name__ == "__main__":
    asyncio.run(update_all_settings())