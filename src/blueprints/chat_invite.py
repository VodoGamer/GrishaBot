from vkbottle.bot import Blueprint, Message

from src.db.models import Chat, User

bp = Blueprint("chat_invite")


async def update_chat(chat_id: int):
    chat_info = (await bp.api.messages.get_conversations_by_id(
        [chat_id])).items[0].chat_settings
    if not chat_info:
        return
    chat = await Chat.get_or_create(id=chat_id)

    chat_members = (await bp.api.messages.get_conversation_members(
        chat[0].id)).items
    for user in chat_members:
        await User.update_or_create(
            {"is_admin": user.is_admin or False,
             "is_owner": user.is_owner or False},
            id=user.member_id, chat=chat[0])


@bp.on.chat_message(text=".init")
async def register_new_chat(message: Message):
    await message.reply("Идёт иницилизация бота")
    await update_chat(message.peer_id)
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
