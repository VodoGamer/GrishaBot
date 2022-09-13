from datetime import datetime, timedelta
from random import choice

from pytz import UTC
from vkbottle.bot import Blueprint, Message

from src.bot.phrases import callingtheuniverse
from src.db.models import Chat, Setting, User
from src.repository.account import is_command_available, get_mention

bp = Blueprint("person of day")


@bp.on.chat_message(regex=r"(?i)^\.*\s*(.+)\s+дня$")
async def person_of_day(message: Message, match, chat: Chat):
    cooldown = is_command_available(chat.last_person_of_day, timedelta(1))

    if cooldown:
        await message.reply(f"Команду можно будет вызвать через {cooldown}")
        return

    chat_members = await bp.api.messages.get_conversation_members(
        message.peer_id)
    if not chat_members.profiles:
        return

    user = await User.get_or_create(chat=chat, id=choice(
        chat_members.profiles).id)
    message_pin = await message.reply(
        f"{choice(callingtheuniverse)} {match[0]} дня это "
        f"{await get_mention(user[0])}")
    chat.last_person_of_day = datetime.now(tz=UTC)
    await chat.save()

    if (await Setting.get(chat=chat, id=1)).value:
        await bp.api.messages.pin(
            chat.id,
            conversation_message_id=message_pin.conversation_message_id)
