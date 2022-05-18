from datetime import datetime
from random import randint
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule
from modules.models import User


bp = Blueprint("Balance")


@bp.on.chat_message(regex=("(?i)^(баланс|б)$"))
async def get_balance(message: Message):
    user = User(message.peer_id, message.from_id)
    await message.reply(f"Баланс {await user.get_mention('gent')} "
                        f"на данный момент: {user.money}")


@bp.on.chat_message(regex=("(?i)^(бонус)$"))
async def get_bonus(message: Message):
    user = User(message.peer_id, message.from_id)
    now = datetime.now()
    bonus = randint(100, 200)
    if user.last_bonus == now.day:
        await message.reply("Бонус можно получить раз в сутки, "
                            "начиная с 00:00")
        return
    user.update_last_bonus(now.day)
    user.change_money(bonus)
    await message.reply(f"{await user.get_mention()} получил {bonus}")


@bp.on.chat_message(
    ReplyMessageRule(),
    regex=("(?i)^(дать|передать|подарить)\s*(денег|баб(ки|ок))?\s*(\d*)$"))
async def send_money(message: Message, match):
    from_user = User(message.peer_id, message.from_id)
    reply_user = User(message.peer_id, message.reply_message.from_id)
    money = int(match[-1])

    if from_user.money < money:
        await message.reply("Недостаточно денег!")
        return
    if not message.from_id == message.reply_message.from_id:
        from_user.change_money(-money)
        reply_user.change_money(money)

    await message.answer(f"{await from_user.get_mention()} передал {money} "
                         f"{await reply_user.get_mention('datv')}")
