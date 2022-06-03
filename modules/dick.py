from datetime import datetime
from random import randint

from vkbottle.bot import Blueprint, Message

from modules.models import Chat, User


bp = Blueprint("Dick")


@bp.on.chat_message(regex=("(?i)^(!|\.|\/)?\s*(писюн|моя пися|пися|член)$"))
async def get_balance(message: Message):
    user = User(message.peer_id, message.from_id)
    await message.reply(f"Писюн {await user.get_mention('gent')} "
                        f"на данный момент: {user.dick_size} см",
                        disable_mentions=True)


@bp.on.chat_message(
    regex=
("(?i)^(!|\.|\/)?\s*(намазать|помазать)\s*(сод(у|ой))?(член|писю)?$"))
async def get_balance(message: Message):
    user = User(message.peer_id, message.from_id)
    now = datetime.now()
    size = randint(-10, 20)
    if user.last_dick == now.day:
        await message.reply("Мазать писюн можно только раз в сутки, "
                            "начиная с 00:00 по мск")
        return
    user.update_last_dick(now.day)
    user.change_dick(size)
    if size > 0:
        word = "увеличился"
    else:
        word = "уменьшился"
        size = str(size)[1:]
    if int(size) == 0:
        await message.reply(f"Писюн {await user.get_mention('gent')} "
                            f"сегодня не изменился",
                            disable_mentions=True)
    else:
        await message.reply(f"Писюн {await user.get_mention('gent')} "
                            f"{word} на {size} см",
                            disable_mentions=True)


@bp.on.chat_message(
    regex="(?i)^(!|\.|\/)?\s*(топ|список)\s*(писюнов|членов)$")
async def top_of_dicks(message: Message, match):
    chat = Chat(message.peer_id)
    if not chat.get_dicks_top():
        await message.reply("Никто не мерится писюнами в этом чате 😔")
        return
    users_mentions = []
    for user in chat.get_dicks_top():
        user_info = User(chat.chat_id, user[0])
        users_mentions.append(
            f"{await user_info.get_mention()} | {user_info.dick_size} см")

    await message.answer(f"топ {match[-1]} в этом чате:\n"
                         "{}".format('\n'.join(users_mentions)),
                         disable_mentions=True)
