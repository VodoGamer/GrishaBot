from random import choice

from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from config import NameCalling
from modules.models import User


bp = Blueprint("Insults")


BeforeTheNameCalling = ["скрывал, что он", "оказывается",
                        "не рассказывал что он"]


@bp.on.chat_message(ReplyMessageRule(), regex=r"(?i)^(!|\.|\/)?\s*обозвать")
async def insult(message: Message):
    user = User(message.peer_id, message.reply_message.from_id)
    await user.init()
    await message.answer(f"{await user.get_mention()} "
                         f"{choice(BeforeTheNameCalling)} "
                         f"{choice(NameCalling)}",
                         disable_mentions=True)
