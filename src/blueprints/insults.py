from random import choice

from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from src.bot.phrases import monikers, notnotified
from src.db.models import User
from src.repository.account import get_mention

bp = Blueprint("Insults")


@bp.on.chat_message(ReplyMessageRule(), regex=r"(?i)^(!|\.|\/)?\s*обозвать")
async def insult(message: Message, user: User):
    await message.answer(f"{await get_mention(user)} "
                         f"{choice(notnotified)} "
                         f"{choice(monikers)}",
                         disable_mentions=True)
