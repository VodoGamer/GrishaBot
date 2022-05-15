from random import choice
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule
from modules.models import User
from config import NameCalling


bp = Blueprint("Insults")


BeforeTheNameCalling = ["скрывал, что он", "оказывается",
                        "не рассказывал что он"]


@bp.on.chat_message(ReplyMessageRule(), regex="(?i)обозвать")
async def insult(message: Message):
    user = User(message.peer_id, message.reply_message.from_id)
    await message.answer(f"{await user.get_mention()} "
                         f"{choice(BeforeTheNameCalling)} "
                         f"{choice(NameCalling)}")
