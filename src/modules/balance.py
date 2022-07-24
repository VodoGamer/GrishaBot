from datetime import datetime, timedelta
from random import randint

from pytz import UTC
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from db.new_models import Chat, User, UserNameCases
from repository.account import get_user_mention

bp = Blueprint("Balance")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(баланс|б)$"))
async def get_balance(message: Message, user: User):
    await message.reply(f"Баланс "
                        f"{await get_user_mention(user, UserNameCases.GEN)} "
                        f"на данный момент: {user.money} 💵",
                        disable_mentions=True)


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(бонус)$"))
async def get_bonus(message: Message, user: User):
    bonus = randint(100, 200)
    now = datetime.now(tz=UTC)

    if user.last_bonus_use:
        db_date_delta = user.last_bonus_use + timedelta(hours=6)
        if db_date_delta > now:
            await message.reply("❌ | Следующий бонус можно получить через "
                                f"{str(db_date_delta - now).split('.', 1)[0]}"
                                )
            return
    user.money += bonus
    user.last_bonus_use = now
    await user.save()

    await message.reply(f"{await get_user_mention(user)} получил {bonus} 💵",
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
        f"{await get_user_mention(user)} "
        f"передал {transferred_money} 💵 "
        f"{await get_user_mention(reply_user, UserNameCases.DAT)}",
        disable_mentions=True
    )


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(список|лист|топ)\s*"
                           r"(форбс|forbes|богачей|денег)?\s*(\d*)$"))
async def get_forbes_list(message: Message, user: User, chat: Chat):
    forbes_list = await User.filter(chat_id=chat.id).exclude(money=0)\
        .order_by('-money')

    if forbes_list:
        users_mentions = []
        for user in forbes_list:
            users_mentions.append(
                f"{await get_user_mention(user)} | {user.money} 💵")
        await message.answer("Список Forbes этой беседы:\n"
                             "{}".format("\n".join(users_mentions)),
                             disable_mentions=True)
    else:
        await message.reply("беседа бомжей :)")
