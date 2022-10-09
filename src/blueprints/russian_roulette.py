import asyncio
from random import randint

from vkbottle import BaseStateGroup
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import CommandRule

from src.db.models import Chat, User

bp = Blueprint("Russian roulette")


class RouleteeState(BaseStateGroup):
    READY = "ready"


@bp.on.chat_message(CommandRule("рулетка", ["."]), state=RouleteeState.READY)
async def try_luck(message: Message, chat: Chat, user: User):
    if randint(1, 5) != 1 or not message.state_peer:
        return "Тебе повезло!"
    if message.state_peer.payload["user_id"] == user.uid:
        await message.reply("Покеда!")
        await asyncio.sleep(3)
        await bp.api.messages.remove_chat_user(chat.id - 2000000000, user.uid)


@bp.on.chat_message(CommandRule("рулетка", ["."]))
async def ask_russian_rouletee(message: Message, chat: Chat, user: User):
    if user.is_admin:
        await message.reply("В этом приколе админы не могут учавствовать :,(")
        return
    await bp.state_dispenser.set(chat.id, RouleteeState.READY, user_id=user.uid)
    await message.reply("Вы уверены?\nЕсли да то напишите эту команду ещё раз")
