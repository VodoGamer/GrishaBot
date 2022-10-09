from vkbottle.bot import Blueprint, Message

from src.blueprints.chat_invite import update_chat_members
from src.bot.setting import SettingType
from src.bot.setting import settings as default_settings
from src.db.models import Chat, Setting, User

bp = Blueprint("Settings")


def convert_to_emoji(setting_value: int):
    if setting_value == 1:
        return "✅"
    elif not setting_value:
        return "❌"
    else:
        return setting_value


@bp.on.chat_message(regex=(r"(?i)^\.*\s*настройки$"))
async def get_settings(message: Message, chat: Chat):
    settings = await Setting.filter(chat=chat).order_by("cid")
    settings_list = [
        f"{setting.cid}. {convert_to_emoji(setting.value)} | "
        f"{default_settings[setting.cid - 1].title}"
        for setting in settings
    ]

    await message.reply(
        "{}\n\nЧтобы изменить настройку напишите:"
        "\n.изменить <номер настройки> <новое значение>\nНапример:\n\n"
        ".изменить 1\n.изменить 4 20".format("\n".join(settings_list))
    )


@bp.on.chat_message(regex=(r"(?i)^\.*\s*(?:изменить|поменять)\s*(\d+)\s*(\d+)?$"))
async def change_setting(message: Message, match, user: User, chat: Chat):
    await update_chat_members(chat)
    if not any((user.is_admin, user.is_owner)):
        await message.reply("❌| Эта команда доступна только админам " "чата!")
        return

    setting = await Setting.get_or_none(cid=match[0], chat=chat)
    if setting is None:
        await message.reply("❌| Неправильно указано правило!")
        return
    setting_config = default_settings[setting.cid - 1]
    if setting_config.type == SettingType.bool:
        setting.value = not setting.value
    else:
        if match[1] is None:
            await message.reply("нет аргумента!")
            return
        if setting_config.max_value < int(match[1]):  # type: ignore
            await message.reply("Макс значение")
            return
        setting.value = match[1]

    await setting.save()
    await message.reply(f"Настройка успешно применена: {convert_to_emoji(setting.value)}")
