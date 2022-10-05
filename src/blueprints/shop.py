"""Магазин бота в беседе"""
from vkbottle import Keyboard, Text
from vkbottle.bot import Blueprint, Message

from src.db.models import Chat

bp = Blueprint("Shop")


@bp.on.chat_message(regex=(r"(?i)магазин?"))
async def open_shop(message: Message, chat: Chat):
    KEYBOARD = Keyboard(inline=True)
    KEYBOARD.add(
        Text(
            "Авто бонус (сбор бонуса по КД)",
            payload={"shop_product": "auto_bonus"},
        )
    )
    KEYBOARD.row()
    KEYBOARD.add(
        Text(
            "Сода (20% больше рост писюна на месяц)",
            payload={"shop_product": "soda"},
        )
    )
    KEYBOARD.row()
    KEYBOARD.add(
        Text(
            "Назначить ник челу на 3 дня",
            payload={"shop_product": "forced_nickname"},
        )
    )

    output_message = await message.answer(
        "Магазин: ", keyboard=KEYBOARD.get_json()
    )
    chat.last_shop_message_id = output_message.conversation_message_id
    await chat.save()


@bp.on.chat_message(payload_map=({"shop_product": str}))
async def product_description(message: Message, chat: Chat):
    KEYBOARD = Keyboard(inline=True)
    KEYBOARD.add(Text("Назад", payload={"shop": "open"}))
    KEYBOARD.row()
    KEYBOARD.add(Text("Назад", payload={"shop_product": "buy"}))

    now_message_id = message.conversation_message_id
    if now_message_id and chat.last_shop_message_id:
        if now_message_id + 10 > chat.last_shop_message_id + 10:
            await message.answer(
                "👆🏻Обновил каталог👆🏻", reply_to=chat.last_shop_message_id
            )

    await bp.api.messages.edit(
        chat.id,
        "Товар123",
        keyboard=KEYBOARD.get_json(),
        conversation_message_id=chat.last_shop_message_id,
    )
