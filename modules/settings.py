from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from modules.models import Settings, User, Chat


bp = Blueprint("Settings")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*настройки"))
async def get_settings(message: Message):
    settings = Settings(message.peer_id)
    list = []
    for i in await settings.get_all():
        if i[3] == "True":
            value = "✅"
        elif i[3] == "False":
            value = "❌"
        elif i[3] != "True" and i[3] != "False":
            value = i[3]
        list.append(f"{value} | {i[1]}")
    result = '\n'.join(list)
    await message.reply(f"{result}\n\nЧтобы изменить команду напишите:"
                        "\n!изменить 'новое значение (если доступно)' "
                        "Закреп сообщений ")


@bp.on.chat_message(
    regex=(r"(?i)^(!|\.|\/)?\s*(изменить|поменять)\s*(\d*)?\s*(.*)"))
async def change_setting(message: Message, match):
    user = User(message.peer_id, message.from_id)
    await user.init()
    chat = Chat(message.peer_id)
    await chat.init()
    if user.is_admin is False:
        if chat.owner_id == message.from_id:
            pass
        else:
            await message.reply("❌| Эта команда доступна только админам "
                                "чата!")
            return

    settings = Settings(message.peer_id)
    if match[-2] != '':
        if int(match[-2]) > 400:
            await message.reply("❌| Максимальное ограничение времени может "
                                "быть 400 сек")
            return
    try:
        result = await settings.change_value(
            (await settings.get_alias_by_setting(match[-1]))[0], match[-2])
        await message.reply(f"{result}| Настройка упешно изменена!")
    except ValueError:
        await message.reply("❌| Неправильно указано значение правила")
    except TypeError:
        await message.reply("❌| Неправильно указано правило")


@bp.on.chat_message(ReplyMessageRule(),
                    regex=(r"(?i)^(!|\.|\/)?\s*назначить\s*админ(ом|а)$"))
async def set_admin(message: Message):
    chat = Chat(message.peer_id)
    await chat.init()

    if chat.owner_id == message.from_id:
        user = User(message.peer_id, message.reply_message.from_id)
        await user.init()
        await user.update_admin("True")
        await message.reply("✅| Админ назначен!\nЧтобы снять админку "
                            "напишите:\nснять админа")


@bp.on.chat_message(ReplyMessageRule(),
                    regex=(r"(?i)^(!|\.|\/)?\s*снять админ(истратора|а)$"))
async def unset_admin(message: Message):
    chat = Chat(message.peer_id)
    await chat.init()

    if chat.owner_id == message.from_id:
        user = User(message.peer_id, message.reply_message.from_id)
        await user.init()
        await user.update_admin(None)
        await message.reply("✅| Админка успешно снята!")
