import re
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import RegexRule, ReplyMessageRule
import modules.models as models

bp = Blueprint("Custom names")


@bp.on.chat_message(RegexRule("(?i)(поменять|изменить|сменить) (ник|имя) (.*)"))
async def change_name(message: Message, match):
    user = models.User(message.peer_id, message.from_id)
    test_custom_name = user.test_custom_name(match[2])
    if test_custom_name is True:
        settings = models.Settings(message.peer_id)
        if settings.get_value("custom_names")[0] == "True":
            if len(match[2].split()) == 1:
                user.set_custom_name(match[2])
                await message.reply("Новое имя успешно установлено!")
            else:
                await message.reply(
                    "Можно устанавливать ник только из одного слова!")
        else:
            await message.reply(
                "Кастомные имена выключены в настройках этого чата!")
    elif test_custom_name == "words!":
        await message.reply("Кастомное имя должно состоять из русских букв!")
    elif test_custom_name == "case!":
        await message.reply("Увы я не смог просклонять ваше имя. "
                            "Попробуйте другое")


@bp.on.chat_message(ReplyMessageRule(), RegexRule("(?i)ник"))
async def get_my_name(message: Message):
    chat = models.Chat(message.peer_id)
    if message.from_id == chat.owner_id:
        user = models.User(message.peer_id, message.reply_message.from_id)
        await message.reply("Имя этого человека на данный момент: "
                             f"{await user.get_name()}")
    else:
        await message.reply("Только админ может писать эту команду!")


@bp.on.chat_message(RegexRule("(?i)(моё имя|мой ник|как меня зовут|ник)"))
async def get_my_name(message: Message):
    user = models.User(message.peer_id, message.from_id)
    await message.reply(f"Ваше имя на данный момент: {await user.get_name()}")
