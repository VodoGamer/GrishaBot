from vkbottle import Keyboard, Text
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import RegexRule, ReplyMessageRule
import modules.models as models


bp = Blueprint("Sex")


@bp.on.chat_message(RegexRule("(?i)секс|посексим"), ReplyMessageRule())
async def new_sex_request(message: Message):
    from_user = models.User(message.peer_id, message.from_id)
    to_user = models.User(message.peer_id, message.reply_message.from_id)
    if to_user.user_id > 0:
        sex = models.Sex(message.peer_id, from_user.user_id)
        if not sex.get_send():
            if not sex.get_request():
                sex.start(to_user.user_id)
                KEYBOARD = Keyboard(inline=True)
                KEYBOARD.add(Text("Согласиться", payload={
                            "sex": "agree"}))
                KEYBOARD.add(Text("Отказаться", payload={
                            "sex": "disagree"}))
                await message.answer(f"{await from_user.get_mention()} "
                                     "предложил поняшиться "
                                     f"{await to_user.get_mention('datv')}",
                                    keyboard=KEYBOARD)
            else:
                await message.answer(f"У {await to_user.get_mention('gent')} "
                                     "есть незаконченный секс\nПопроси его "
                                     "поскорее потрахаться")
        else:
            await message.reply("У тебя есть незаконченный секс\nЧтобы "
                                "закончить его напиши -секс")
    else:
        await message.answer(f"{await from_user.get_mention()} ёбнулся и "
                             "начал ебать бота "
                             f"{await to_user.get_mention('gent')}👳‍♂️")


@bp.on.chat_message(payload={"sex": "agree"})
async def sex_agree(message: Message):
    pass


@bp.on.chat_message(payload={"sex": "disagree"})
async def sex_disagree(message: Message):
    from_user = models.User(message.peer_id, message.from_id)
    sex = models.Sex(message.peer_id, from_user.user_id)
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

    partner_info = models.User(message.peer_id, partner)
    print(await from_user.get_sex())
    if await from_user.get_sex() == 1:
        await message.answer(f"{await from_user.get_mention()} отказалась "
                             "от секса с "
                             f"{await partner_info.get_mention('ablt')}")
    else:
        await message.answer(f"{await from_user.get_mention()} отказался "
                             "от секса с "
                             f"{await partner_info.get_mention('ablt')}")


@bp.on.chat_message(RegexRule("(?i)-секс"))
async def discard_sex_request(message: Message):
    from_user = models.User(message.peer_id, message.from_id)
    sex = models.Sex(message.peer_id, from_user.user_id)
    try:
        sex.discard_sex()
        sex.end_sex(sex.get_send())
        await message.reply(f"{await from_user.get_mention()} "
                            "завершил все запросы на секс")
    except:
        await message.reply(f"Ты собрался завершать то, чего нет?")

