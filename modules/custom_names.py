from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from modules.models import User, Settings


bp = Blueprint("Custom names")


@bp.on.chat_message(ReplyMessageRule(), regex=(r"(?i)^(!|\.|\/)?\s*ник"))
async def get_his_name(message: Message):
    user = User(message.peer_id, message.reply_message.from_id)
    await user.init()
    await message.reply("Имя этого человека на данный момент: "
                        f"{await user.get_name()}")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(моё имя|мой ник"
                           r"|как меня зовут|ник)$"))
async def get_my_name(message: Message):
    user = User(message.peer_id, message.from_id)
    await user.init()
    await message.reply(f"Ваше имя на данный момент: {await user.get_name()}")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*(поменять|изменить|сменить)?"
                           r"\s*(ник|имя)\s*(.*)"))
async def change_name(message: Message, match):
    user = User(message.peer_id, message.from_id)
    await user.init()
    test_custom_name = await user.test_custom_name(match[-1])
    if test_custom_name is True:
        settings = Settings(message.peer_id)
        if (await settings.get_value("custom_names"))[0] == "True":
            if len(match[-1].split()) == 1:
                await user.set_custom_name(match[-1])
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
    elif test_custom_name == "words_count!":
        await message.reply("Длина имени должна быть не более 35 символов!")
