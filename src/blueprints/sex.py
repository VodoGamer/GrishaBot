import asyncio
import json
from random import choice, randint

from vkbottle import Keyboard, Text
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from src.db.models import Chat, User
from src.repository.account import Case, get_mention

bp = Blueprint("sex")
bp.labeler.vbml_ignore_case = True


@bp.on.chat_message(ReplyMessageRule(), text=("секс", "посексим"))
async def new_sex_request(message: Message, chat: Chat, user: User):
    reply_id = message.reply_message.from_id  # type: ignore

    KEYBOARD = Keyboard(inline=True)

    KEYBOARD.add(Text("Согласиться", payload={"sex_agree": f"{user.uid}_{reply_id}"}))
    KEYBOARD.add(Text("Отказаться", payload={"sex_disagree": f"{user.uid}_{reply_id}"}))

    to_user = await User.get(chat_id=chat.id, uid=reply_id)
    await message.answer(
        f"{await get_mention(user)} предложил "
        f"поняшиться {await get_mention(to_user, Case.DATIVE)}",
        keyboard=KEYBOARD.get_json(),
        disable_mentions=True,
    )


@bp.on.chat_message(payload_map={"sex_agree": str})
async def sex_agree(message: Message, chat: Chat):
    payload = json.loads(message.payload)["sex_agree"]  # type: ignore
    payloads = str(payload).split("_")
    from_id = payloads[0]
    to_id = payloads[1]

    if message.from_id != int(to_id):
        return

    # Inits
    sex_sender = await User.get(chat_id=chat.id, uid=from_id)
    sex_recipient = await User.get(chat_id=chat.id, uid=to_id)

    words = [
        "поняшиться😊",
        "в кровать🛏",
        "в постель🛏",
        "потрахаться🔞",
        "порвать попку😖",
        "порвать пизду😖",
    ]
    await message.answer(
        f"{await get_mention(sex_sender)} соблазнил "
        f"{await get_mention(sex_recipient, Case.ACCUSATIVE)} "
        f"{choice(words)}",
        disable_mentions=True,
    )
    await asyncio.sleep(2)
    if randint(1, 3) == 1:
        await message.answer(
            f"{await get_mention(sex_sender)} и "
            f"{await get_mention(sex_recipient)} "
            "начали раздеваться",
            disable_mentions=True,
        )
    else:
        words = ["начал снимать одежду👙 с", "начал разрывать одежду👙"]
        await message.answer(
            f"{await get_mention(sex_sender)} "
            f"{choice(words)} "
            f"{await get_mention(sex_recipient, Case.ACCUSATIVE)}",
            disable_mentions=True,
        )
    await asyncio.sleep(3)
    await message.answer(
        f"После долгих раздумий "
        f"{await get_mention(sex_sender)} и "
        f"{await get_mention(sex_recipient)} "
        f"выбрали секс в позе {randint(1, 100)}",
        "photo-194020282_457239082",
        disable_mentions=True,
    )
    await asyncio.sleep(3)
    words = [
        "ноги🦵",
        "ножки🦵",
        "ухо👂",
        "нос👃",
        "пятки🦶",
        "сосок🔞",
        "сиськи🔞",
        "руки🖐",
        "пизду🔞",
        "член🔞",
        "анальную дырочку🔞",
        "ладошку🖐",
    ]
    await message.answer(
        f"{await get_mention(sex_sender)} облизал "
        f"{choice(words)} "
        f"{await get_mention(sex_recipient, Case.GENITIVE)}",
        disable_mentions=True,
    )
    await asyncio.sleep(2)
    if randint(1, 4) == 1:
        await message.answer(
            f"{await get_mention(sex_sender)} делает "
            "нежный кунилингус "
            f"{await get_mention(sex_recipient, Case.DATIVE)}",
            disable_mentions=True,
        )
    else:
        await message.answer(
            f"{await get_mention(sex_recipient)} делает "
            "минет "
            f"{await get_mention(sex_sender, Case.DATIVE)}",
            disable_mentions=True,
        )
    await asyncio.sleep(2)
    await message.answer(
        f"{await get_mention(sex_sender)} "
        f"вставил свои {sex_sender.dick_size} "
        f"см в {await get_mention(sex_recipient, Case.GENITIVE)} 😖",
        disable_mentions=True,
    )
    await asyncio.sleep(3)
    if randint(1, 5) != 1:
        words = ["попку", "писечку", "пизду"]
        await message.answer(
            f"{await get_mention(sex_sender)} "
            f"порвал {choice(words)} "
            f"{await get_mention(sex_recipient, Case.GENITIVE)} 😖",
            disable_mentions=True,
        )
        return
    await message.answer(
        f"{await get_mention(sex_sender)} "
        "кончил в "
        f"{await get_mention(sex_recipient, Case.ACCUSATIVE)} 😳",
        disable_mentions=True,
    )
    if randint(1, 2) == 1:
        await message.answer(
            f"У {await get_mention(sex_sender, Case.GENITIVE)} "
            f"и {await get_mention(sex_recipient, Case.GENITIVE)} "
            "появился ребёнок 😳",
            disable_mentions=True,
        )


@bp.on.chat_message(payload_map={"sex_disagree": str})
async def sex_disagree(message: Message, user: User, chat: Chat):
    payload = json.loads(message.payload)["sex_disagree"]  # type: ignore
    payloads = str(payload).split("_")
    from_id = payloads[0]
    to_id = payloads[1]

    if message.from_id != int(to_id):
        return

    to_user = user
    from_user = await User.get(chat_id=chat.id, uid=from_id)

    await message.answer(
        f"{await get_mention(to_user)} отказал в сексе который ему "
        f"предложил(а) {await get_mention(from_user)}",
        disable_mentions=True,
    )
