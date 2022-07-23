from tortoise.exceptions import DoesNotExist
from vkbottle.bot import Blueprint, Message

from db.new_models import Chat, Setting, User

bp = Blueprint("Settings")


def convert_to_emoji(setting_value: int | bool):
    if setting_value == 1:
        return "✅"
    elif not setting_value:
        return "❌"
    else:
        return setting_value


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*настройки"))
async def get_settings(message: Message, chat: Chat):
    result = []
    settings = await Setting.filter(chat_id=chat.id).prefetch_related(
        'chat__settings')
    for setting in settings:
        setting_value = convert_to_emoji(setting.value)

        result.append(f"{setting.id}. {setting_value} | {setting.title}")
    result = "\n".join(result)
    await message.reply(f"{result}\n\nЧтобы изменить настройку напишите:"
                        "\n!изменить <номер настройки> <новое значение>\n"
                        "Например:\n\n!изменить 1")


@bp.on.chat_message(
    regex=(r"(?i)^(!|\.|\/)?\s*(изменить|поменять)\s*(\d*)\s*(.*)?$"))
async def change_setting(message: Message, match, user: User):

    if not user.is_admin:
        await message.reply("❌| Эта команда доступна только админам "
                            "чата!")
        return

    try:
        setting = await Setting.get(id=match[-2])
        if setting.max_value == 1:
            if match[-1] != '':
                await message.reply("❌| Для этого правила не надо передавать "
                                    "дополнительное значение!")
                return
        else:
            if match[-1] == '':
                await message.reply("❌| Не передано новое значение для "
                                    "правила!")
                return
            if int(match[-1]) > setting.max_value:
                await message.reply("❌| Максимальное значение для этого "
                                    f"правила: {setting.max_value}")
                return

        if setting.max_value == 1:
            setting.value = 1 if setting.value == 0 else 0
            await message.reply(f"✅| Настройка успешно изменена на: "
                                f"{convert_to_emoji(setting.value)}")
        else:
            setting.value = int(match[-1])
            await message.reply(f"✅| Настройка успешно изменена на: "
                                f"{setting.value}")
        await setting.save()
    except DoesNotExist:
        await message.reply("❌| Неправильно указано правило!")
