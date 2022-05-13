from vkbottle.dispatch.rules.base import RegexRule
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import RegexRule
from modules.models import User, Casino, CasinoUser

bp = Blueprint("Rp commands")


@bp.on.chat_message(RegexRule("^(\d*) (к|б|ч|з)$"))
async def new_bet(message: Message, match):
    user = User(message.peer_id, message.from_id)
    if user.money is not None:  # фолбек
        if user.money > int(match[0]):
            user_casino = CasinoUser(user.chat_id, user.user_id)
            user_casino.register(int(match[0]), match[1])
            user.change_money(-int(match[0]))
            await message.reply("Ставка защитана!")
    else:
        await message.reply("Недостаточно денег для ставки!")
