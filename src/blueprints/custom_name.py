from pytrovich.enums import Case
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from src.db.models import Chat, User
from src.repository.account import get_mention, get_name

bp = Blueprint("Custom name")


@bp.on.chat_message(ReplyMessageRule(), regex=(r"(?i)^\.*\s*ник|имя$"))
async def get_his_name(message: Message, chat: Chat):
    user = await User.get(chat=chat, uid=message.reply_message.from_id)  # type: ignore

    await message.reply(
        f"Ник {await get_mention(user, Case.GENITIVE, custom_name=False)}:\n"
        f"{await get_name(user)}",
        disable_mentions=True,
    )


@bp.on.chat_message(regex=(r"(?i)^\.*\s*(мо(й|ё)\s*(ник|имя))$"))
async def get_my_name(message: Message, user: User):
    await message.answer(
        f"Ник {await get_mention(user, Case.GENITIVE, custom_name=False)}:\n"
        f"{await get_name(user)}",
        disable_mentions=True,
    )


@bp.on.chat_message(
    regex=(r"(?i)^(!|\.|\/)?\s*(поменять|изменить|сменить)?" r"\s*(ник|имя)\s*(.*)")
)
async def change_name(message: Message, match, user: User):
    new_name = match[-1]

    if len(new_name) > 35:
        await message.reply("Имя должно быть не более 35 символов!")
        return

    await message.reply("Имя успешно изменено!")
    user.custom_name = new_name.capitalize()
    await user.save()
