from datetime import datetime, timedelta
from random import randint

from pytz import UTC
from vkbottle.bot import Blueprint, Message

from src.db.models import Chat, User
from src.repository.account import (Case, command_not_available, get_mention,
                                    get_top_list)

bp = Blueprint("Dick")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(писюн|моя пися|пися|член)$"))
async def get_balance(message: Message, user: User):
    await message.reply(f"Писюн "
                        f"{await get_mention(user, Case.GENITIVE)} "
                        f"на данный момент: {user.dick_size} см",
                        disable_mentions=True)


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(намазать|помазать)\s*"
                           r"(сод(у|ой))?(член|писю)?$"))
async def dick_height(message: Message, user: User):
    cooldown = command_not_available(user.last_dick_growth_use, timedelta(1))
    size = randint(-10, 20)

    if cooldown:
        await message.reply(f"Писюн можно будет помазать через {cooldown}")
        return

    user.dick_size += size
    user.last_dick_growth_use = datetime.now(tz=UTC)
    await user.save()

    visual_size = abs(size)
    if size > 0:
        word = f"увеличился на {visual_size}"
    elif size == 0:
        word = "не изменился"
    else:
        word = f"уменьшился на {visual_size}"

    await message.reply(
        f"Писюн {await get_mention(user, Case.GENITIVE)} {word}",
        disable_mentions=True)


@bp.on.chat_message(regex=r"(?i)^(!|\.|\/)?\s*(топ|список)\s*"
                    r"(писюнов|членов)$")
async def top_of_dicks(message: Message, match, user: User, chat: Chat):
    dicks_list = await User.filter(chat_id=chat.id).exclude(dick_size=0)\
        .order_by('-dick_size')
    top = await get_top_list(dicks_list)

    if top:
        await message.answer(f"топ {match[-1]} в этом чате:\n {top}",
                             disable_mentions=True)
    else:
        await message.reply("Никто не мерится писюнами в этом чате 😔")
