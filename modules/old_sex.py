import asyncio
from random import choice, randint
import sqlite3
from vkbottle.bot import Blueprint, Message, rules
from vkbottle import Keyboard, Text


bp = Blueprint("old_sex")


class Sex():
    def __init__(self, peer_id: int) -> None:
        self.db = "db.db"
        self.peer_id = peer_id

        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()

    def start(self, message_id: int, partner_1: int, partner_2: int) -> None:
        '''Функция, записывающая в БД приглашение заняться сексом'''

        self.cursor.execute(
            f"INSERT INTO sex (peer_id, message_id, partner_1, partner_2) VALUES ({self.peer_id}, {message_id}, {partner_1}, {partner_2})")
        self.connection.commit()

    def check(self, partner_1: int) -> bool:
        '''Проверяет есть ли запрос на секс у переданного пользователя'''

        self.cursor.execute(
            f"SELECT * FROM sex WHERE partner_2 = {partner_1} AND peer_id={self.peer_id}")

        if self.cursor.fetchone() is None:
            return False
        else:
            return True

    def get_partner(self, partner_1: int) -> int:
        '''Находит партнёра'''

        self.cursor.execute(
            f"SELECT * FROM sex WHERE peer_id = {self.peer_id} AND partner_1 = {partner_1} OR partner_2 = {partner_1}")
        result = self.cursor.fetchone()
        if result[3] == partner_1:
            return result[2]
        else:
            return result[3]

    def FORCE_end(self, user_id: int) -> None:
        '''Удаляет навсегда строку о предложении заняться сексом '''

        self.cursor.execute(
            f"DELETE FROM sex WHERE peer_id = {self.peer_id} AND partner_1 = {user_id} OR partner_2 = {user_id}")
        self.connection.commit()

    def end(self, partner_1: int, partner_2: int) -> None:
        '''Удаляет навсегда строку о предложении заняться сексом '''

        self.cursor.execute(
            f"DELETE FROM sex WHERE peer_id = {self.peer_id} AND partner_1 = {partner_1} AND partner_2 = {partner_2}")
        self.connection.commit()


@bp.on.chat_message(rules.ReplyMessageRule(), rules.RegexRule("секс|посексим"))
async def kiss(message: Message):
    KEYBOARD = Keyboard(inline=True)
    KEYBOARD.add(Text("Согласиться", payload={"sex": "agree"}))
    KEYBOARD.add(Text("Отказаться", payload={"sex": "disagree"}))

    r_id = message.from_id + message.conversation_message_id
    goal_id = message.reply_message.from_id
    sex = Sex(message.peer_id)

    if goal_id > 0:
        goal_info = await bp.api.users.get(goal_id)
        if not sex.check(message.from_id):
            if not sex.check(message.reply_message.from_id):
                sex.start(message.conversation_message_id, message.from_id, message.reply_message.from_id)
                await message.answer(f"@id{goal_id} ({goal_info[0].first_name}) тебе предложили посексить", keyboard=KEYBOARD, random_id=r_id)
            else:
                goal_info = await bp.api.users.get(goal_id, name_case="gen")
                await message.reply(f"У @id{goal_id} ({goal_info[0].first_name}) есть незаконченный брак, попроси его поскорее потрахаться")
        else:
            await message.answer('У тебя ещё есть незаконченый секс\nДля того чтобы его закончить напиши "-секс"', random_id=r_id)
    else:
        user = await bp.api.users.get(message.from_id)
        await message.answer(f"@id{message.from_id} ({user[0].first_name}) начал ебать бота. ЛЁХА ИДИ НАХУЙ")


@bp.on.chat_message(rules.RegexRule("-секс"))
async def minus_sex(message: Message):
    r_id = message.from_id + message.conversation_message_id
    sex = Sex(message.peer_id)

    sex.FORCE_end(message.from_id)
    await message.answer("Ты закончил секс", random_id=r_id)


@bp.on.chat_message(payload={"sex": "agree"})
async def sex_handler(message: Message):
    sex = Sex(message.peer_id)

    if sex.check(message.from_id):
        partner_1 = sex.get_partner(message.from_id)
        partner_2 = message.from_id
        sex.end(partner_1, partner_2)
        r_id = 0

        partner_1_info = await bp.api.users.get(partner_1)
        partner_1_dat = await bp.api.users.get(partner_1, name_case="dat")

        partner_2_info = await bp.api.users.get(partner_2)
        partner_2_acc = await bp.api.users.get(partner_2, name_case="acc")
        partner_2_gen = await bp.api.users.get(partner_2, name_case="gen")
        partner_2_dat = await bp.api.users.get(partner_2, name_case="dat")

        await message.answer(f"@id{partner_1} ({partner_1_info[0].first_name}) соблазнил @id{partner_2} ({partner_2_acc[0].first_name}) в постель😏🛏", random_id=r_id)
        await asyncio.sleep(randint(2, 4))

        random = randint(1, 2)
        if random == 1:
            words = ['начал раздевать👚', 'начал снимать одежду👚']
            await message.answer(f"@id{partner_1} ({partner_1_info[0].first_name}) {choice(words)} @id{partner_2} ({partner_2_acc[0].first_name})", random_id=r_id)
        else:
            await message.answer(f"@id{partner_1} ({partner_1_info[0].first_name}) и @id{partner_2} ({partner_2_info[0].first_name}) начали раздеваться🥵", random_id=r_id)
        await asyncio.sleep(randint(3, 5))

        words = ["руки🖐", "ноги🦶", "пятки🦶", "пизду🔞", "сиськи🔞", "сосок🔞"]
        await message.answer(f"@id{partner_1} ({partner_1_info[0].first_name}) облизал {choice(words)} @id{partner_2} ({partner_2_gen[0].first_name})", random_id=r_id)
        await asyncio.sleep(randint(3, 5))

        random = randint(1, 2)
        if random == 1:
            await message.answer(f"@id{partner_1} ({partner_1_info[0].first_name}) делает нежный кунилингус😛 @id{partner_2} ({partner_2_dat[0].first_name})", random_id=r_id)
        else:
            await message.answer(f"@id{partner_2} ({partner_2_info[0].first_name}) делает минет😛 @id{partner_1} ({partner_1_dat[0].first_name})", random_id=r_id)
        await asyncio.sleep(randint(3, 5))

        if randint(1, 4) == 1:
            await message.answer(f"@id{partner_1} ({partner_1_info[0].first_name}) и @id{partner_2} ({partner_2_info[0].first_name}) выбрали анальный секс🥵", random_id=r_id)
            await asyncio.sleep(randint(3, 5))
            await message.answer(f"@id{partner_1} ({partner_1_info[0].first_name}) порвал попку @id{partner_2} ({partner_2_gen[0].first_name})😖", random_id=r_id)
        else:
            await message.answer(f"@id{partner_1} ({partner_1_info[0].first_name}) вставил член в пизду @id{partner_2} ({partner_2_gen[0].first_name})🔞", random_id=r_id)
            if randint(1, 4) == 1:
                await message.answer(f"@id{partner_1} ({partner_1_info[0].first_name}) достал членом до матки @id{partner_2} ({partner_2_gen[0].first_name})😫", random_id=r_id)
            if randint(1, 5) == 1:
                await asyncio.sleep(5)
                await message.answer(f"@id{partner_1} ({partner_1_info[0].first_name}) кончил в @id{partner_2} ({partner_2_acc[0].first_name})", random_id=r_id)


@bp.on.chat_message(payload={"sex": "disagree"})
async def sex_disagree(message: Message):
    sex = Sex(message.peer_id)

    if sex.check(message.from_id):
        r_id = message.from_id + message.conversation_message_id
        user = await bp.api.users.get(message.from_id, fields="sex")

        sex.end(sex.get_partner(message.from_id), message.from_id)
        photo = choice(["photo-194020282_457239081", "video-194020282_456239018"])
        if user[0].sex.value == 1:
            await message.answer(f"@id{user[0].id} ({user[0].first_name}) отказалась от секса", photo, r_id)
        else:
            await message.answer(f"@id{user[0].id} ({user[0].first_name}) отказался от секса", photo, r_id)
