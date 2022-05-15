from datetime import datetime
from random import randint
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import RegexRule
from modules.models import User


bp = Blueprint("Balance")


@bp.on.chat_message(RegexRule("(?i)^(баланс|б)$"))
async def get_balance(message: Message):
    user = User(message.peer_id, message.from_id)
    await message.reply(f"Баланс {await user.get_mention('gent')} "
                        f"на данный момент: {user.money}")


@bp.on.chat_message(RegexRule("(?i)^(бонус)$"))
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
