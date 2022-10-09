from datetime import datetime, timedelta
from random import randint
from pytz import UTC

from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from src.bot.phrases import command_not_availabale_now, not_enough_money
from src.bot.stickers import rich_stickers, send_sticker
from src.db.models import Chat, User, UserBonus
from src.repository.account import (
    Case,
    TopType,
    get_mention,
    get_top_list,
    is_command_available,
)

bp = Blueprint("Balance")


@bp.on.chat_message(regex=(r"(?i)^\.*\s*б(аланс)?$"))
async def get_balance(message: Message, user: User, chat: Chat):
    await message.reply(
        f"Баланс {await get_mention(user, Case.GENITIVE)}: {user.money} 💵",
        disable_mentions=True,
    )
    await send_sticker(message, chat, rich_stickers)


@bp.on.chat_message(regex=(r"(?i)^\.*\s*бонус$"))
async def get_bonus(message: Message, user: User, chat: Chat):
    bonus = randint(100, 200)
    last_bonus = (await UserBonus.filter(user=user).order_by("id"))
    add_bonus = 0

    if last_bonus != []:
        cooldown = is_command_available(
            last_bonus[-1].date, timedelta(hours=6))
        if not cooldown[0]:
            return (command_not_availabale_now.format(time=cooldown[1]))
        if last_bonus[-1].date + timedelta(hours=12) > datetime.now(UTC):
            add_bonus = round((bonus / 100) * 10)
    user.money += bonus + add_bonus
    await user.save()
    await UserBonus.create(bonus_value=bonus, user=user)

    await message.reply(
        f"{await get_mention(user)} получил {bonus} + {add_bonus or '0'} 💵\n"
        "Чтобы получить + 10 % к бонусу, используйте команду в течение 12 "
        "часов =)",
        disable_mentions=True
    )
    await send_sticker(message, chat, rich_stickers)


@bp.on.chat_message(
    ReplyMessageRule(),
    regex=(r"(?i)^\.*\s*(?:(?:пере)?дать|подарить)\s*(\d+)$"),
)
async def send_money(message: Message, match, user: User, chat: Chat):
    reply_user = await User.get(
        uid=message.reply_message.from_id, chat=chat  # type: ignore
    )
    transferred_money = int(match[0])

    if user.money < transferred_money:
        await message.reply(not_enough_money)
        return
    if user.uid != reply_user.uid:
        user.money -= transferred_money
        await user.save()

        reply_user.money += transferred_money
        await reply_user.save()

    await message.answer(
        f"{await get_mention(user)} "
        f"передал {transferred_money} 💵 "
        f"{await get_mention(reply_user, Case.DATIVE)}",
        disable_mentions=True,
    )


@bp.on.chat_message(
    regex=(r"(?i)^\.*\s*(список|лист|топ)\s*(форбс|forbes|богачей|денег)$")
)
async def get_forbes_list(message: Message, chat: Chat):
    forbes_list = (
        await User.filter(chat=chat).exclude(money=0).order_by("-money")
    )
    top = await get_top_list(forbes_list, TopType.money)

    if top:
        await message.answer(
            f"Список Forbes беседы:\n {top}", disable_mentions=True
        )
    else:
        await message.reply("беседа бомжей :)")
