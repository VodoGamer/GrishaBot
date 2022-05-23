from datetime import datetime, timedelta
from random import randint
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule
from modules.models import User


bp = Blueprint("Balance")


@bp.on.chat_message(regex=("(?i)^(!|\.|\/)?\s*(баланс|б)$"))
async def get_balance(message: Message):
    user = User(message.peer_id, message.from_id)
    await message.reply(f"Баланс {await user.get_mention('gent')} "
                        f"на данный момент: {user.money} 💵",
                        disable_mentions=True)


@bp.on.chat_message(regex=("(?i)^(!|\.|\/)?\s*(бонус)$"))
async def get_bonus(message: Message):
    user = User(message.peer_id, message.from_id)
    bonus = randint(100, 200)

    now = datetime.now()
    if user.bonus_date:
        db_date = datetime.strptime(user.bonus_date, "%Y-%m-%d %X.%f")
        db_date_delta = db_date + timedelta(hours=6)
    else:
        db_date = False

    if db_date:
        if db_date_delta > now:
            await message.reply("❌ | Следующий бонус можно получить "
                                f"{str(db_date_delta).split('.')[0]}")
            return
    user.update_last_bonus(now)
    user.change_money(bonus)
    await message.reply(f"{await user.get_mention()} получил {bonus}")


@bp.on.chat_message(
    ReplyMessageRule(),
    regex=
("(?i)^(!|\.|\/)?\s*(дать|передать|подарить)\s*(денег|баб(ки|ок))?\s*(\d*)$"))
async def send_money(message: Message, match):
    from_user = User(message.peer_id, message.from_id)
    reply_user = User(message.peer_id, message.reply_message.from_id)
    money = int(match[-1])

    if from_user.money < money:
        await message.reply("❌ | Недостаточно денег!")
        return
    if not message.from_id == message.reply_message.from_id:
        from_user.change_money(-money)
        reply_user.change_money(money)

    await message.answer(f"{await from_user.get_mention()} передал {money} 💵"
                         f"{await reply_user.get_mention('datv')}",
                         disable_mentions=True)
