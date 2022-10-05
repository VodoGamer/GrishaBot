from vkbottle.bot import Blueprint, Message

from src.db.models import Chat, User

bp = Blueprint("Stat")


@bp.on.chat_message(regex=(r"(?i)^\.*\s*моя\s+стат(?:а)?|статистика$"))
async def get_own_stats(message: Message, user: User):
    await message.reply(
        f"Вы написали в данной беседе {user.messages_count} " "сообщений"
    )


@bp.on.chat_message(regex=(r"(?i)^\.*\s*стат(а)?|статистика$"))
async def get_chat_stats(message: Message, chat: Chat):
    await message.reply(
        f"За всё время в этой беседе написали "
        f"{chat.messages_count} сообщений"
    )
