from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import VBMLRule, RegexRule
import modules.models as models

bp = Blueprint("Rp commands")


@bp.on.chat_message(RegexRule("(поменять|изменить|сменить) (ник|имя) (.*)"))
async def change_name(message: Message, match):
    user = models.User(message.peer_id, message.from_id)
    user.set_custom_name(match[2])
    await message.reply("Новое имя успешно установлено!")


@bp.on.chat_message(RegexRule("(моё имя|мой ник|как меня зовут)"))
async def get_my_name(message: Message):
    user = models.User(message.peer_id, message.from_id)
    await message.reply(f"Ваше имя на данный момент: {await user.get_name()}")


@bp.on.chat_message(RegexRule("(ни(к))"))
async def get_my_name(message: Message, match):
    print(match)
