from datetime import datetime
from random import randint
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import RegexRule
from modules.models import User


bp = Blueprint("Dick")


@bp.on.chat_message(RegexRule("(?i)^(!|\.)?\s*(писюн|моя пися|пися|член)$"))
async def get_balance(message: Message):
    user = User(message.peer_id, message.from_id)
    await message.reply(f"Писюн {await user.get_mention('gent')} "
                        f"на данный момент: {user.dick_size} см")


@bp.on.chat_message(
    RegexRule("(?i)^(!|\.)?\s*(намазать сод(у|ой)|намазать (член|писю))$"))
async def get_balance(message: Message):
    user = User(message.peer_id, message.from_id)
    now = datetime.now()
    size = randint(-10, 20)
    if user.last_dick == now.day:
        await message.reply("Мазать писюн можно только раз в сутки, "
                            "начиная с 00:00")
        return
    user.update_last_dick(now.day)
    user.change_dick(size)
    await message.reply(f"Писюн {await user.get_mention('gent')} "
                        f"изменился на {size} см")
