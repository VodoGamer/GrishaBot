from datetime import datetime
from random import choice

from vkbottle.bot import Blueprint, Message

from modules.models import Chat, Settings, User
from modules.phrases import callingtheuniverse

bp = Blueprint("Person of day")


@bp.on.chat_message(regex=r"(?i)^(!|\.|\/)?\s*(.*)\s{1,}дня$")
async def change_name(message: Message, match):
    chat = Chat(message.peer_id)
    await chat.init()
    now = datetime.now()
    if chat.last_person_send != now.day or chat.last_person_send is None:
        users = await bp.api.messages.get_conversation_members(
                peer_id=message.peer_id)
        users_id = []
        for i in users.profiles:
            users_id.append(i.id)
        user = User(chat.chat_id, choice(users_id))
        await user.init()
        output = await message.reply(f"{choice(callingtheuniverse)} "
                                     f"{match[-1]} дня это "
                                     f"{await user.get_mention()}")
        await chat.set_last_person_send(now.day)
        setting = Settings(chat.chat_id)
        if (await setting.get_value("pin"))[0] == "True":
            await bp.api.messages.pin(
                chat.chat_id,
                conversation_message_id=output.conversation_message_id)
    else:
        await message.reply("Команду можно использовать один раз в сутки "
                            "начиная с 00:00 по мск.")
