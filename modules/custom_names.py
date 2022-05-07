from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import RegexRule, ReplyMessageRule
import modules.models as models

bp = Blueprint("Rp commands")


@bp.on.chat_message(RegexRule("(поменять|изменить|сменить) (ник|имя) (.*)"))
async def change_name(message: Message, match):
    user = models.User(message.peer_id, message.from_id)
    if len(match[2].split()) == 1:
        user.set_custom_name(match[2])
        await message.reply("Новое имя успешно установлено!")
    else:
        await message.reply("Можно устанавливать ник только из одного слова!")



@bp.on.chat_message(RegexRule("(моё имя|мой ник|как меня зовут)"))
async def get_my_name(message: Message):
    user = models.User(message.peer_id, message.from_id)
    await message.reply(f"Ваше имя на данный момент: {await user.get_name()}")


@bp.on.chat_message(ReplyMessageRule(), RegexRule("ник"))
async def get_my_name(message: Message):
    chat = models.Chat(message.peer_id)
    if message.from_id == chat.owner_id:
        user = models.User(message.peer_id, message.reply_message.from_id)
        await message.reply(f"Имя этого человека на данный момент: {await user.get_name()}")
    else:
        await message.reply("Только админ может писать эту команду!")

