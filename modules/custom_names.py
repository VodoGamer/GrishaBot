from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule
from modules.models import User, Settings


bp = Blueprint("Custom names")


@bp.on.chat_message(ReplyMessageRule(), regex=("(?i)^(!|\.|\/)?\s*ник"))
async def get_my_name(message: Message):
    user = User(message.peer_id, message.reply_message.from_id)
    await message.reply("Имя этого человека на данный момент: "
                        f"{await user.get_name()}")


@bp.on.chat_message(
    regex=("(?i)^(!|\.|\/)?\s*(моё имя|мой ник|как меня зовут|ник)$"))
async def get_my_name(message: Message):
    user = User(message.peer_id, message.from_id)
    await message.reply(f"Ваше имя на данный момент: {await user.get_name()}")


@bp.on.chat_message(regex=(
    "(?i)^(!|\.|\/)?\s*(поменять|изменить|сменить)?\s*(ник|имя)\s*(.*)"))
async def change_name(message: Message, match):
    user = User(message.peer_id, message.from_id)
    test_custom_name = user.test_custom_name(match[-1])
    if test_custom_name is True:
        settings = Settings(message.peer_id)
        if settings.get_value("custom_names")[0] == "True":
            if len(match[-1].split()) == 1:
                user.set_custom_name(match[-1])
                await message.reply("✅| Новое имя успешно установлено!")
            else:
                await message.reply(
                    "❌| Можно устанавливать ник только из одного слова!")
        else:
            await message.reply(
                "❌| Кастомные имена выключены в настройках этого чата!")
    elif test_custom_name == "words!":
        await message.reply("Кастомное имя должно состоять из русских букв!")
    elif test_custom_name == "case!":
        await message.reply("Увы я не смог просклонять ваше имя. "
                            "Попробуйте другое")
