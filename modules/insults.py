from random import choice

from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from modules.models import User
from phrases import notnotified, monikers


bp = Blueprint("Insults")


@bp.on.chat_message(ReplyMessageRule(), regex=r"(?i)^(!|\.|\/)?\s*обозвать")
async def insult(message: Message):
    user = User(message.peer_id, message.reply_message.from_id)
    await user.init()
    await message.answer(f"{await user.get_mention()} "
                         f"{choice(notnotified)} "
                         f"{choice(monikers)}",
                         disable_mentions=True)
