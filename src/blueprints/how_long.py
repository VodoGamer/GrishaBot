from random import choice, randint

from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from src.bot.phrases import notnotified, notnotified_multi
from src.db.models import Chat, User
from src.repository.account import get_mention

bp = Blueprint("How Long")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)\s*я\s*(.*)"))
async def how_long_i(message: Message, match, user: User):
    await message.answer(f"{await get_mention(user)} "
                         f"{choice(notnotified)} "
                         f"{match[-1]} на {randint(0, 100)}%",
                         disable_mentions=True)


@bp.on.chat_message(ReplyMessageRule(),
                    regex=(r"(?i)^(!|\.|\/)\s*(он|она|оно)\s*(.*)"))
async def how_long_he(message: Message, match, chat: Chat):
    user = await User.get(
        chat_id=chat.id,
        id=message.reply_message.from_id)  # type: ignore

    await message.answer(f"{await get_mention(user)}"
                         f" {choice(notnotified)} "
                         f"{match[-1]} на {randint(0, 100)}%",
                         disable_mentions=True)


@bp.on.chat_message(ReplyMessageRule(), regex=(r"(?i)^(!|\.|\/)\s*мы\s*(.*)"))
async def how_long_we(message: Message, match, user: User, chat: Chat):
    user_2 = await User.get(
        chat_id=chat.id,
        id=message.reply_message.from_id)  # type: ignore

    await message.answer(f"{await get_mention(user)} и "
                         f"{await get_mention(user_2)} "
                         f"{choice(notnotified_multi)} {match[-1]} "
                         f"на {randint(0, 100)}%",
                         disable_mentions=True)
