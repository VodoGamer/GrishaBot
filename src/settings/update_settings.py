from loguru import logger

from src.db.models import Chat, Setting
from src.settings.settings import settings


async def update_chat_settings(chat: Chat):
    for setting in settings:
        await Setting.get_or_create(
            {"value": setting.default_value},
            chat=chat, cid=setting.id)


async def update_all_settings():
    for chat in await Chat.all().prefetch_related():
        await update_chat_settings(chat)
        logger.debug(f"settings of {chat.id} chat updated!")
