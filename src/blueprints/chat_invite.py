from vkbottle.bot import Blueprint, Message

from src.db.models import Chat, User
from src.settings.update_settings import update_chat_settings

bp = Blueprint("chat_invite")


async def update_chat(chat_id: int) -> tuple[Chat, bool]:
    chat_info = (await bp.api.messages.get_conversations_by_id(
        [chat_id])).items[0].chat_settings
    if not chat_info:
        raise AttributeError(f"{chat_id} dont have any information on VK API")
    chat = await Chat.get_or_create(id=chat_id)
    return chat


async def update_chat_members(chat: Chat):
    chat_members = (await bp.api.messages.get_conversation_members(
        chat.id)).items
    for user in chat_members:
        await User.update_or_create(
            {"is_admin": user.is_admin or False,
             "is_owner": user.is_owner or False},
            uid=user.member_id, chat=chat)


@bp.on.chat_message(regex=r"(?i)^\.\s*init$")
async def register_new_chat(message: Message):
    await message.reply("Идёт иницилизация бота")
    chat = await update_chat(message.peer_id)
    await update_chat_settings(chat[0])
    await update_chat_members(chat[0])
    await message.reply("Иницилизация завершена!")


@bp.on.chat_message(action="chat_invite_user")
async def init_new_chat(message: Message):
    if not message.action:
        return
    if not message.action.member_id:
        return

    if message.action.member_id > 0:
        await update_chat(message.peer_id)
        return "Привет мешок с костями!"
    group = (await bp.api.groups.get_by_id())[0]
    if message.action.member_id != -group.id:
        await update_chat(message.peer_id)
        return "Привет брат робот!"
    return (
        "Спасибо за приглашение! Для начала работы мне "
        "нужны права администратора\nПосле того как вы "
        "их предоставите напишите команду: \".init\"")
