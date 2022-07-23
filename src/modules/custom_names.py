import re

from pymorphy2 import MorphAnalyzer
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from db.new_models import Chat, User, get_user_name

bp = Blueprint("Custom names")
morph = MorphAnalyzer()


@bp.on.chat_message(ReplyMessageRule(), regex=(r"(?i)^(!|\.|\/)?\s*ник|имя$"))
async def get_his_name(message: Message, chat: Chat):
    user = await User.get(chat_id=chat.id,
                          id=message.reply_message.from_id)  # type: ignore
    await message.reply("Имя этого человека на данный момент: "
                        f"{await get_user_name(user)}")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(моё имя|мой ник"
                           r"|как меня зовут|ник)$"))
async def get_my_name(message: Message, user: User):
    await message.reply(f"Ваше имя на данный момент: "
                        f"{await get_user_name(user)}")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(поменять|изменить|сменить)?"
                           r"\s*(ник|имя)\s*(.*)"))
async def change_name(message: Message, match, user: User):
    new_name = match[-1]

    if len(new_name) > 35:
        await message.reply("Имя должно быть не более 35 символов!")
    if not re.search("^[а-я]+", new_name):
        await message.reply("Имя должно состоять только из русских символов!")
    try:
        raw_name = morph.parse(new_name)[0]
        cases = ["nomn", "gent", "datv",
                 "accs", "ablt", "loct", "voct"]
        for case in cases:
            raw_name.inflect(  # type: ignore
                {case}).word.capitalize()
        await message.reply("Имя успешно изменено!")

        user.custom_name = new_name
        await user.save()
    except AttributeError:
        await message.reply("Имя не склоняется! Поробуйте другое.")
