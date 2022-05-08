from datetime import datetime
from random import choice
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import RegexRule
import modules.models as models

bp = Blueprint("Person of day")


phrases = ["Ящитаю что", "Мне кажется", "Вселенная подсказала что"]
@bp.on.chat_message(RegexRule("(.*) дня"))
async def change_name(message: Message, match):
    chat = models.Chat(message.peer_id)
    now = datetime.now()
    if chat.last_person_send != now.day or chat.last_person_send == None:
        users = await bp.api.messages.get_conversation_members(peer_id=message.peer_id)
        users_id = []
        for i in users.profiles:
            users_id.append(i.id)
        user = models.User(chat.chat_id,choice(users_id))
        output = await message.reply(f"{choice(phrases)} {match[0]} дня это {await user.get_mention()}")
        chat.set_last_person_send(now.day)
        await bp.api.messages.pin(chat.chat_id, conversation_message_id=output.conversation_message_id)
    else:
        await message.reply("Команду можно использовать один раз в сутки начиная с 00:00.")
