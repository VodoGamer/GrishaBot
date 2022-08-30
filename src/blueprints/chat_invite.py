from vkbottle_types.objects import MessagesMessageActionStatus
from vkbottle.bot import Blueprint, Message

from src.db.models import Chat, User

bp = Blueprint("chat_invite")


@bp.on.chat_message(text=".init")
async def register_new_chat(message: Message):
    await message.reply("Идёт иницилизация бота")
    chat_info = (await bp.api.messages.get_conversations_by_id(
        [message.peer_id])).items[0].chat_settings
    if not chat_info:
        return

    chat = await Chat.create(
        id=message.peer_id,
        owner_id=chat_info.owner_id)

    chat_members = (await bp.api.messages.get_conversation_members(
        chat.id)).items

    for user in chat_members:
        await User.create(id=user.member_id,
                          chat=chat,
                          is_admin=user.is_admin or False)
    await message.reply("Иницилизация завершена!")


@bp.on.chat_message()
async def init_new_chat(message: Message):
    if not message.action:
        return
    if message.action.type == MessagesMessageActionStatus.CHAT_INVITE_USER:
        await message.answer("Спасибо за приглашение! Для начала работы мне "
                             "нужны права администратора\nПосле того как вы "
                             "их предоставите напишите команду: \".init\"")
