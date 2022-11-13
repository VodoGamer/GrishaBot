from datetime import datetime, timedelta
from random import randint

from pytrovich.enums import Case
from pytz import UTC
from vkbottle.bot import Blueprint, Message

from src.db.models import Chat, User
from src.repository.account import TopType, get_mention, get_top_list, is_command_available

bp = Blueprint("dick")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(писюн|моя пися|пися|член)$"))
async def get_balance(message: Message, user: User):
    await message.reply(
        f"Писюн {await get_mention(user, Case.GENITIVE)}:\n" f"{user.dick_size} см",
        disable_mentions=True,
    )


@bp.on.chat_message(
    regex=(r"(?i)^(!|\.|\/)?\s*(намазать|помазать)\s*" r"(сод(у|ой))?(член|писю)?$")
)
async def dick_height(message: Message, user: User):
    cooldown = is_command_available(user.last_dick_growth_use, timedelta(1))
    resize = randint(-10, 20)

    if not cooldown[0]:
        await message.reply(f"Писюн можно будет помазать через {cooldown[1]}")
        return

    user.dick_size += resize
    user.last_dick_growth_use = datetime.now(tz=UTC)
    await user.save()

    visual_size = abs(resize)
    if resize > 0:
        word = f"увеличился на {visual_size}"
    elif resize == 0:
        word = "не изменился"
    else:
        word = f"уменьшился на {visual_size}"

    await message.reply(
        f"Писюн {await get_mention(user, Case.GENITIVE)} {word}",
        disable_mentions=True,
    )


@bp.on.chat_message(regex=r"(?i)^\.*\s*(?:топ|список)\s*(писюнов|членов)$")
async def top_of_dicks(message: Message, match, chat: Chat):
    dicks_list = await User.filter(chat_id=chat.id).exclude(dick_size=0).order_by("-dick_size")
    top = await get_top_list(dicks_list, TopType.dicks)

    if top:
        await message.answer(f"Топ {match[0]} в этом чате:\n {top}", disable_mentions=True)
    else:
        await message.reply("Никто не мерится писюнами в этом чате 😔")
