from datetime import datetime, timedelta
from random import choice

from pytz import UTC
from vkbottle.bot import Blueprint, Message

from src.bot.phrases import callingtheuniverse
from src.db.models import Chat, Setting, User
from src.repository.account import command_not_available, get_mention

bp = Blueprint("Person of day")


@bp.on.chat_message(regex=r"(?i)^(!|\.|\/)?\s*(.*)\s{1,}дня$")
async def person_of_day(message: Message, match, chat: Chat):
    cooldown = command_not_available(chat.last_person_of_day_use, timedelta(1))

    if cooldown:
        await message.reply(f"Команду можно будет вызвать через {cooldown}")
        return

    chat_members = await bp.api.messages.get_conversation_members(
        peer_id=message.peer_id)
    users_id = []
    for member in chat_members.profiles:
        users_id.append(member.id)

    user = await User.get(chat_id=chat.id, id=choice(users_id))

    message_pin = await message.reply(f"{choice(callingtheuniverse)} "
                                      f"{match[-1]} дня это "
                                      f"{await get_mention(user)}")
    chat.last_person_of_day_use = datetime.now(tz=UTC)
    await chat.save()

    if (await Setting.get(chat_id=chat.id, id=1)).value:
        await bp.api.messages.pin(
            chat.id,
            conversation_message_id=message_pin.conversation_message_id)
