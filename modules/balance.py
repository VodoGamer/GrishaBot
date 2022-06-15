from datetime import datetime, timedelta
from random import randint

from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from modules.models import Chat, User


bp = Blueprint("Balance")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(баланс|б)$"))
async def get_balance(message: Message):
    user = User(message.peer_id, message.from_id)
    await user.init()
    await message.reply(f"Баланс {await user.get_mention('gent')} "
                        f"на данный момент: {user.money} 💵",
                        disable_mentions=True)


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(бонус)$"))
async def get_bonus(message: Message):
    user = User(message.peer_id, message.from_id)
    await user.init()
    bonus = randint(100, 200)

    now = datetime.now()
    if user.bonus_date:
        db_date = datetime.strptime(user.bonus_date, "%Y-%m-%d %X.%f")
        db_date_delta = db_date + timedelta(hours=6)

        if db_date_delta > now:
            await message.reply("❌ | Следующий бонус можно получить "
                                f"{str(db_date_delta).split('.')[0]} по мск")
            return
    await user.update_last_bonus(now)
    await user.change_money(bonus)
    await message.reply(f"{await user.get_mention()} получил {bonus} 💵",
                        disable_mentions=True)


@bp.on.chat_message(
    ReplyMessageRule(),
    regex=(r"(?i)^(!|\.|\/)?\s*(дать|передать|подарить)\s*(денег|баб(ки|ок))"
           r"?\s*(\d*)$"))
async def send_money(message: Message, match):
    from_user = User(message.peer_id, message.from_id)
    reply_user = User(message.peer_id, message.reply_message.from_id)
    await from_user.init()
    await reply_user.init()
    money = int(match[-1])

    if from_user.money < money:
        await message.reply("❌ | Недостаточно денег!")
        return
    if not message.from_id == message.reply_message.from_id:
        await from_user.change_money(-money)
        await reply_user.change_money(money)

    await message.answer(f"{await from_user.get_mention()} передал {money} 💵"
                         f"{await reply_user.get_mention('datv')}",
                         disable_mentions=True)


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(список|лист|топ)\s*"
                           r"(форбс|forbes|богачей|денег)?\s*(\d*)$"))
async def get_forbes_list(message: Message):
    chat = Chat(message.peer_id)
    await chat.init()

    if chat.get_forbes_list():
        users_mentions = []
        for user in await chat.get_forbes_list():
            user_info = User(chat.chat_id, user[0])
            await user_info.init()
            users_mentions.append(
                f"{await user_info.get_mention()} | {user_info.money} 💵")
        await message.answer("Список Forbes этой беседы:\n"
                             "{}".format("\n".join(users_mentions)),
                             disable_mentions=True)
    else:
        await message.reply("беседа бомжей :)")
