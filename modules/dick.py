from datetime import datetime
from random import randint
from vkbottle.bot import Blueprint, Message
from modules.models import User


bp = Blueprint("Dick")


@bp.on.chat_message(regex=("(?i)^(!|\.)?\s*(писюн|моя пися|пися|член)$"))
async def get_balance(message: Message):
    user = User(message.peer_id, message.from_id)
    await message.reply(f"Писюн {await user.get_mention('gent')} "
                        f"на данный момент: {user.dick_size} см")


@bp.on.chat_message(
regex=("(?i)^(!|\.)?\s*(намазать|помазать сод(у|ой)|член|писю)$"))
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
    if size > 0:
        word = "увеличился"
    else:
        word = "уменьшился"
        size = str(size)[1:]
    if size == 0:
        await message.reply(f"Писюн {await user.get_mention('gent')} "
                            f"сегодня не изменился")
    else:
        await message.reply(f"Писюн {await user.get_mention('gent')} "
                            f"{word} на {size} см")
