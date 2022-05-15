from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule
import modules.models as models


bp = Blueprint("Settings")


@bp.on.chat_message(regex=("(?i)!настройки"))
async def get_settings(message: Message):
    settings = models.Settings(message.peer_id)
    tuple = []
    for i in settings.get_all():
        if i[3] == "True": bool = "✅"
        if i[3] == "False": bool = "❌"
        tuple.append(f"{bool} | {i[1]}")
    result = '\n'.join(tuple)
    await message.reply(f"{result}\n\nЧтобы изменить команду напишите:"
                        "\n!изменить Закреп сообщений")


@bp.on.chat_message(regex=("(?i)!(изменить) (.*)"))
async def change_setting(message: Message, match):
    user = models.User(message.peer_id, message.from_id)
    chat = models.Chat(message.peer_id)
    if user.is_admin is False:
        if chat.owner_id == message.from_id:
            pass
        else:
            await message.reply("❌Эта команда доступна только админам чата!")
            return

    settings = models.Settings(message.peer_id)
    try:
        result = settings.change_value(
            settings.get_alias_by_setting(match[1])[0])
        await message.reply(f"{result}| Настройка упешно изменена!")
    except:
        await message.reply("❌Неправильно указано правило")


@bp.on.chat_message(ReplyMessageRule(), regex=("(?i)^назначить админ(ом|а)$"))
async def set_admin(message: Message):
    chat = models.Chat(message.peer_id)

    if chat.owner_id == message.from_id:
        user = models.User(message.peer_id, message.reply_message.from_id)
        user.update_admin("True")
        await message.reply("✅ Админ назначен!\nЧтобы снять админку напишите:\n"
                            "снять админа")


@bp.on.chat_message(ReplyMessageRule(),
                    regex=("(?i)^снять админ(истратора|а)$"))
async def set_admin(message: Message):
    chat = models.Chat(message.peer_id)

    if chat.owner_id == message.from_id:
        user = models.User(message.peer_id, message.reply_message.from_id)
        user.update_admin(None)
        await message.reply("✅ Админка успешно снята!")
