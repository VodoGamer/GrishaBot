from random import choice, randint
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import RegexRule, ReplyMessageRule
import modules.models as models


bp = Blueprint("How Long")

phrases = ["не рассказывал что он", "скрывал что он", "рассказал что он"]
phrases_multi = ["не рассказывали что они", "скрывали что они", "рассказали что они"]


@bp.on.chat_message(RegexRule("(!|\/\|.)я (.*)"))
async def how_long_i(message: Message, match):
    user = models.User(message.peer_id, message.from_id)
    await message.answer(f"{await user.get_mention()} {choice(phrases)} {match[-1]} на {randint(0, 100)}%")


@bp.on.chat_message(RegexRule("(!|\/\|.)(он|она|оно) (.*)"), ReplyMessageRule())
async def how_long_he(message: Message, match):
    user = models.User(message.peer_id, message.reply_message.from_id)
    await message.answer(f"{await user.get_mention()} {choice(phrases)} {match[-1]} на {randint(0, 100)}%")


@bp.on.chat_message(RegexRule("(!|\/\|.)мы (.*)"), ReplyMessageRule())
async def how_long_we(message: Message, match):
    user_1 = models.User(message.peer_id, message.from_id)
    user_2 = models.User(message.peer_id, message.reply_message.from_id)
    await message.answer(f"{await user_1.get_mention()} и {await user_2.get_mention()} {choice(phrases_multi)} {match[-1]} на {randint(0, 100)}%")
