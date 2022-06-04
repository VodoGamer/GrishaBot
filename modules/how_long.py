from random import choice, randint

from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from modules.models import User


bp = Blueprint("How Long")


phrases = ["не рассказывал что он", "скрывал что он", "рассказал что он"]
phrases_multi = ["не рассказывали что они", "скрывали что они",
                 "рассказали что они"]


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)\s*я\s*(.*)"))
async def how_long_i(message: Message, match):
    user = User(message.peer_id, message.from_id)
    await message.answer(f"{await user.get_mention()} {choice(phrases)} "
                         f"{match[-1]} на {randint(0, 100)}%",
                         disable_mentions=True)


@bp.on.chat_message(ReplyMessageRule(),
                    regex=(r"(?i)^(!|\.|\/)\s*(он|она|оно)\s*(.*)"))
async def how_long_he(message: Message, match):
    user = User(message.peer_id, message.reply_message.from_id)
    await message.answer(f"{await user.get_mention()} {choice(phrases)} "
                         f"{match[-1]} на {randint(0, 100)}%",
                         disable_mentions=True)


@bp.on.chat_message(ReplyMessageRule(), regex=(r"(?i)^(!|\.|\/)\s*мы\s*(.*)"))
async def how_long_we(message: Message, match):
    user_1 = User(message.peer_id, message.from_id)
    user_2 = User(message.peer_id, message.reply_message.from_id)
    await message.answer(f"{await user_1.get_mention()} и "
                         f"{await user_2.get_mention()} "
                         f"{choice(phrases_multi)} {match[-1]} "
                         f"на {randint(0, 100)}%",
                         disable_mentions=True)
