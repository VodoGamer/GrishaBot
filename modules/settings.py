from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import CommandRule, RegexRule, ReplyMessageRule
import modules.models as models


bp = Blueprint("Settings")


@bp.on.chat_message(CommandRule("настройки"))
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


@bp.on.chat_message(RegexRule("(?i)!(изменить) (.*)"))
async def change_setting(message: Message, match):
    user = models.User(message.peer_id, message.from_id)
    chat = models.Chat(message.peer_id)
    if chat.owner_id != message.from_id or user.is_admin == False:
        await message.reply("❌Эта команда доступна только админам чата!")
        return

    settings = models.Settings(message.peer_id)
    try:
        result = settings.change_value(
            settings.get_alias_by_setting(match[1])[0])
        await message.reply(f"{result}| Настройка упешно изменена!")
    except:
        await message.reply("❌Неправильно указано правило")

@bp.on.chat_message(RegexRule("(?i)^назначить админ(ом|а)$"),
                    ReplyMessageRule())
async def set_admin(message: Message):
    chat = models.Chat(message.peer_id)

    if chat.owner_id == message.from_id:
        user = models.User(message.peer_id, message.reply_message.from_id)
        user.update_admin("True")
        await message.reply("✅ Админ назначен!\nЧтобы снять админку напишите:\n"
                            "снять админа")


@bp.on.chat_message(RegexRule("(?i)^снять админ(истратора|а)$"),
                    ReplyMessageRule())
async def set_admin(message: Message):
    chat = models.Chat(message.peer_id)

    if chat.owner_id == message.from_id:
        user = models.User(message.peer_id, message.reply_message.from_id)
        user.update_admin(None)
        await message.reply("✅ Админка успешно снята!")
