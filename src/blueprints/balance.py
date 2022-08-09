from datetime import datetime, timedelta
from random import randint

from pytz import UTC
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from src.db.models import Chat, User
from src.repository.account import (Case, TopType, command_not_available,
                                    get_mention, get_top_list)

bp = Blueprint("Balance")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(баланс|б)$"))
async def get_balance(message: Message, user: User):
    await message.reply(f"Баланс "
                        f"{await get_mention(user, Case.GENITIVE)} "
                        f"на данный момент: {user.money} 💵",
                        disable_mentions=True)


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(бонус)$"))
async def get_bonus(message: Message, user: User):
    bonus = randint(100, 200)
    cooldown = command_not_available(user.last_bonus_use, timedelta(hours=6))

    if cooldown:
        await message.reply("❌ | Следующий бонус можно получить через "
                            f"{cooldown}"
                            )
        return
    user.money += bonus
    user.last_bonus_use = datetime.now(tz=UTC)
    await user.save()

    await message.reply(f"{await get_mention(user)} получил {bonus} 💵",
                        disable_mentions=True)


@bp.on.chat_message(
    ReplyMessageRule(),
    regex=(r"(?i)^(!|\.|\/)?\s*(дать|передать|подарить)\s*(денег|баб(ки|ок))"
           r"?\s*(\d*)$"))
async def send_money(message: Message, match, user: User, chat: Chat):
    reply_user = await User.get(
        id=message.reply_message.from_id,  # type: ignore
        chat_id=chat.id)
    # reply_message.from_id будет передан всегда из-за `ReplyMessageRule()`
    transferred_money = int(match[-1])

    if user.money < transferred_money:
        await message.reply("❌ | Недостаточно денег!")
        return
    if not user.id == reply_user.id:
        user.money -= transferred_money
        await user.save()

        reply_user.money += transferred_money
        await reply_user.save()

    await message.answer(
        f"{await get_mention(user)} "
        f"передал {transferred_money} 💵 "
        f"{await get_mention(reply_user, Case.DATIVE)}",
        disable_mentions=True
    )


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(список|лист|топ)\s*"
                           r"(форбс|forbes|богачей|денег)?\s*(\d*)$"))
async def get_forbes_list(message: Message, chat: Chat):
    forbes_list = await User.filter(chat_id=chat.id).exclude(money=0)\
        .order_by('-money')
    top = await get_top_list(forbes_list, TopType.money)

    if top:
        await message.answer(f"Список Forbes этой беседы:\n {top}",
                             disable_mentions=True)
    else:
        await message.reply("беседа бомжей :)")
