from vkbottle.bot import Blueprint, Message

from modules.models import User, Chat


bp = Blueprint("Stat")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?моя\s{0,}стат(а)?|статистика$"))
async def get_own_stats(message: Message):
    user = User(message.peer_id, message.from_id)
    await message.reply(f"Вы написали в данной беседе {user.messages} "
                        "сообщений")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?стат(а)?|статистика$"))
async def get_own_stats(message: Message):
    chat = Chat(message.peer_id)
    await message.reply(f"За всё время в этой беседе написали "
                        f"{chat.messages} сообщений")
