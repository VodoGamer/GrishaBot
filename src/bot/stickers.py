from random import choice

from vkbottle.bot import Message

from src.db.models import Chat, Setting


async def send_sticker(
    message: Message, chat: Chat, stickers: list[int] | tuple
):
    if (await Setting.get(cid=4, chat=chat)).value:
        await message.answer(sticker_id=choice(stickers))


rich_stickers = (58263, 18503, 96)
sad_stickers = (70873, 59)
