from random import choice, randint
import asyncio

from vkbottle import Keyboard, Text
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import RegexRule, ReplyMessageRule

from modules.models import User, Sex


bp = Blueprint("Sex")


@bp.on.chat_message(RegexRule("(?i)секс|посексим"), ReplyMessageRule())
async def new_sex_request(message: Message):
    from_user = User(message.peer_id, message.from_id)
    to_user = User(message.peer_id, message.reply_message.from_id)
    if to_user.user_id < 0:
        # Проверка на группу
        await message.answer(f"{await from_user.get_mention()} ёбнулся и "
                             "начал ебать "
                             f"{await to_user.get_mention('gent')}👳‍♂️")
        return
    sex = Sex(message.peer_id, from_user.user_id)
    if sex.get_send():
        # Проверка на незаконченный секс у отправителя
        await message.reply("У тебя есть незаконченный секс\nЧтобы "
                            "закончить его напиши -секс")
        return
    if sex.get_request():
        # Проверка на незаконченный секс у получателя
        await message.answer(f"У {await to_user.get_mention('gent')} "
                             "есть незаконченный секс\nПопроси его "
                             "поскорее потрахаться")
        return
    # Если всё хорошо
    sex.start(to_user.user_id)
    KEYBOARD = Keyboard(inline=True)
    KEYBOARD.add(Text("Согласиться", payload={"sex": "agree"}))
    KEYBOARD.add(Text("Отказаться", payload={"sex": "disagree"}))
    await message.answer(f"{await from_user.get_mention()} предложил "
                         f"поняшиться {await to_user.get_mention('datv')}",
                         keyboard=KEYBOARD)


@bp.on.chat_message(payload={"sex": "agree"})
async def sex_agree(message: Message):
    # Inits
    sex = Sex(message.peer_id, message.from_id)
    if sex.get_request() is None:
        return
    sex_recipient = User(message.peer_id, sex.from_user)
    sex_sender = User(message.peer_id, sex.get_request())
    sex.discard_sex()

    words = ("поняшиться😊", "в кровать🛏", "в постель🛏", "потрахаться🔞",
             "порвать попку😖", "порвать пизду😖")
    await message.answer(f"{await sex_sender.get_mention()} соблазнил "
                         f"{await sex_recipient.get_mention('accs')} "
                         f"{choice(words)}",
                         disable_mentions=True)
    await asyncio.sleep(2)
    if randint(1, 3) == 1:
        await message.answer(f"{await sex_sender.get_mention()} и "
                             f"{await sex_recipient.get_mention()} "
                             "начали раздеваться",
                             disable_mentions=True)
    else:
        words = ("начал снимать одежду👙 с", "начал разрывать одежду👙")
        await message.answer(f"{await sex_sender.get_mention()} "
                             f"{choice(words)} "
                             f"{await sex_recipient.get_mention('accs')}",
                             disable_mentions=True)
    await asyncio.sleep(3)
    await message.answer(f"После долгих раздумий "
                         f"{await sex_sender.get_mention()} и "
                         f"{await sex_recipient.get_mention()} "
                         f"выбрали секс в позе {randint(1, 100)}",
                         "photo-194020282_457239082",
                         disable_mentions=True)
    await asyncio.sleep(3)
    words = ("ноги🦵", "ножки🦵", "ухо👂", "нос👃", "пятки🦶", "сосок🔞", "сиськи🔞",
             "руки🖐", "пизду🔞", "член🔞", "анальную дырочку🔞", "ладошку🖐")
    await message.answer(f"{await sex_sender.get_mention()} облизал "
                         f"{choice(words)} "
                         f"{await sex_recipient.get_mention('gent')}",
                         disable_mentions=True)
    await asyncio.sleep(2)
    if randint(1, 4) == 1:
        await message.answer(f"{await sex_sender.get_mention()} делает "
                             "нежный кунилингус "
                             f"{await sex_recipient.get_mention('datv')}",
                             disable_mentions=True)
    else:
        await message.answer(f"{await sex_recipient.get_mention()} делает "
                             "минет "
                             f"{await sex_sender.get_mention('datv')}",
                             disable_mentions=True)
    await asyncio.sleep(2)
    await message.answer(f"{await sex_sender.get_mention()} "
                         f"вставил свои {sex_sender.dick_size} "
                         f"см в {await sex_recipient.get_mention('gent')} 😖",
                         disable_mentions=True)
    await asyncio.sleep(3)
    if randint(1, 5) != 1:
        words = ("попку", "писечку", "пизду")
        await message.answer(f"{await sex_sender.get_mention()} "
                             f"порвал {choice(words)} "
                             f"{await sex_recipient.get_mention('gent')} 😖",
                             disable_mentions=True)
        return
    await message.answer(f"{await sex_sender.get_mention()} "
                         "кончил в "
                         f"{await sex_recipient.get_mention('accs')} 😳",
                         disable_mentions=True)
    if randint(1, 2) == 1:
        await message.answer(f"У {await sex_sender.get_mention('gent')} "
                             f"и {await sex_recipient.get_mention('gent')} "
                             "появился ребёнок 😳",
                             disable_mentions=True)


@bp.on.chat_message(payload={"sex": "disagree"})
async def sex_disagree(message: Message):
    from_user = User(message.peer_id, message.from_id)
    sex = Sex(message.peer_id, from_user.user_id)
    requset = sex.get_request()
    send = sex.get_send()
    if requset is None and send is None:
        return
    elif requset is None:
        partner = send
        sex.end_sex(partner)
    else:
        partner = requset
        sex.discard_sex()

    partner_info = User(message.peer_id, partner)
    if await from_user.get_sex() == 1:
        await message.answer(f"{await from_user.get_mention()} отказалась "
                             "от секса с "
                             f"{await partner_info.get_mention('ablt')}")
    else:
        await message.answer(f"{await from_user.get_mention()} отказался "
                             "от секса с "
                             f"{await partner_info.get_mention('ablt')}")


@bp.on.chat_message(RegexRule(r"(?i)-\s{0,}секс"))
async def discard_sex_request(message: Message):
    from_user = User(message.peer_id, message.from_id)
    sex = Sex(message.peer_id, from_user.user_id)
    sex.discard_sex()
    sex.end_sex(sex.get_send())
    await message.reply(f"{await from_user.get_mention()} "
                        "завершил все запросы на секс")
