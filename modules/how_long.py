from random import choice, randint

from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from modules.models import User
from modules.phrases import notnotified, notnotified_multi

bp = Blueprint("How Long")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)\s*я\s*(.*)"))
async def how_long_i(message: Message, match):
    user = User(message.peer_id, message.from_id)
    await user.init()
    await message.answer(f"{await user.get_mention()} {choice(notnotified)} "
                         f"{match[-1]} на {randint(0, 100)}%",
                         disable_mentions=True)


@bp.on.chat_message(ReplyMessageRule(),
                    regex=(r"(?i)^(!|\.|\/)\s*(он|она|оно)\s*(.*)"))
async def how_long_he(message: Message, match):
    user = User(message.peer_id, message.reply_message.from_id)
    await user.init()
    await message.answer(f"{await user.get_mention()} {choice(notnotified)} "
                         f"{match[-1]} на {randint(0, 100)}%",
                         disable_mentions=True)


@bp.on.chat_message(ReplyMessageRule(), regex=(r"(?i)^(!|\.|\/)\s*мы\s*(.*)"))
async def how_long_we(message: Message, match):
    user_1 = User(message.peer_id, message.from_id)
    await user_1.init()
    user_2 = User(message.peer_id, message.reply_message.from_id)
    await user_2.init()
    await message.answer(f"{await user_1.get_mention()} и "
                         f"{await user_2.get_mention()} "
                         f"{choice(notnotified_multi)} {match[-1]} "
                         f"на {randint(0, 100)}%",
                         disable_mentions=True)
