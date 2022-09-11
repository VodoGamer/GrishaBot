from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from src.db.models import Setting, User
from src.repository.account import Case, get_mention

bp = Blueprint("Rp commands")
bp.labeler.auto_rules = [ReplyMessageRule()]


@bp.on.chat_message(regex=(r"(?i)(ударить|ёбнуть)\s*(.*)?"))
async def to_kick(message: Message, match, user: User):
    await Rp(message, "ударил", match[-1], user,
             "photo-194020282_457239111").send_message()


@bp.on.chat_message(regex=(r"(?i)(обдристать)\s*(.*)?"))
async def poooooo(message: Message, match, user: User):
    await Rp(message, "обдристал", match[-1], user,
             "photo-194020282_457239089").send_message()


@bp.on.chat_message(regex=(r"(?i)(выебать|трахнуть)\s*(.*)?"))
async def fuck(message: Message, match, user: User):
    await Rp(message, "выебал", match[-1], user,
             "photo-194020282_457239085").send_message()


@bp.on.chat_message(regex=(r"(?i)(уебать)\s*(.*)?"))
async def to_fuck_off(message: Message, match, user: User):
    await Rp(message, "уебал", match[-1], user,
             "photo-194020282_457239112").send_message()


@bp.on.chat_message(regex=(r"(?i)(кончить)\s*(.*)?"))
async def cum(message: Message, match, user: User):
    await Rp(message, "обкончал", match[-1], user,
             "photo-194020282_457239090").send_message()


@bp.on.chat_message(regex=(r"(?i)(отсосать)\s*(.*)?"))
async def suck_it(message: Message, match, user: User):
    await Rp(message, "отсосал у", match[-1], user,
             "photo-194020282_457239097").send_message()


@bp.on.chat_message(regex=(r"(?i)(обнять|прижать)\s*(.*)?"))
async def hug(message: Message, match, user: User):
    await Rp(message, "обнял", match[-1], user,
             "photo-194020282_457239092").send_message()


@bp.on.chat_message(regex=(r"(?i)(засосать)\s*(.*)?"))
async def suck(message: Message, match, user: User):
    await Rp(message, "засосал", match[-1], user,
             "photo-194020282_457239086").send_message()


@bp.on.chat_message(regex=(r"(?i)(п.рнуть)\s*(.*)?"))
async def fart(message: Message, match, user: User):
    await Rp(message, "пёрнул на", match[-1], user,
             "photo-194020282_457239098").send_message()


@bp.on.chat_message(regex=(r"(?i)(о(т|тт)рахать)\s*(.*)?"))
async def fuck_strong(message: Message, match, user: User):
    await Rp(message, "обтрахал", match[-1], user,
             "photo-194020282_457239094").send_message()


@bp.on.chat_message(regex=(r"(?i)(убить)\s*(.*)?"))
async def kill(message: Message, match, user: User):
    await Rp(message, "убил", match[-1], user,
             "photo-194020282_457239110").send_message()


@bp.on.chat_message(regex=(r"(?i)(послать)\s*(.*)?"))
async def fuck_off(message: Message, match, user: User):
    await Rp(message, "послал", match[-1], user,
             "photo-194020282_457239104").send_message()


@bp.on.chat_message(regex=(r"(?i)(шлёпнуть)\s*(.*)?"))
async def slap(message: Message, match, user: User):
    await Rp(message, "шлёпнул", match[-1], user,
             "photo-194020282_457239113").send_message()


@bp.on.chat_message(regex=(r"(?i)(пнуть)\s*(.*)?"))
async def kick(message: Message, match, user: User):
    await Rp(message, "пнул", match[-1], user,
             "photo-194020282_457239100").send_message()


@bp.on.chat_message(regex=(r"(?i)(сжечь)\s*(.*)?"))
async def burn(message: Message, match, user: User):
    await Rp(message, "сжёг", match[-1], user,
             "photo-194020282_457239107").send_message()


@bp.on.chat_message(regex=(r"(?i)(понюхать)\s*(.*)?"))
async def smell_it(message: Message, match, user: User):
    await Rp(message, "понюхал", match[-1], user,
             "photo-194020282_457239103").send_message()


@bp.on.chat_message(regex=(r"(?i)(лизнуть|облизать|полизать)\s*(.*)?"))
async def lick(message: Message, match, user: User):
    await Rp(message, "облизал", match[-1], user,
             "photo-194020282_457239091").send_message()


@bp.on.chat_message(regex=(r"(?i)(отлизать)\s*(.*)?"))
async def lick_it_off(message: Message, match, user: User):
    await Rp(message, "отлизал", match[-1], user,
             "photo-194020282_457239096", Case.GENITIVE).send_message()


@bp.on.chat_message(regex=(r"(?i)(погладить)\s*(.*)?"))
async def stroke(message: Message, match, user: User):
    await Rp(message, "погладил", match[-1], user,
             "photo-194020282_457239101").send_message()


@bp.on.chat_message(regex=(r"(?i)(обо(с|сс)ать)\s*(.*)?"))
async def piss_on(message: Message, match, user: User):
    await Rp(message, "обоссал", match[-1], user,
             "photo-194020282_457239093").send_message()


@bp.on.chat_message(regex=(r"(?i)(плюнуть)\s*(.*)?"))
async def spit(message: Message, match, user: User):
    await Rp(message, "плюнул в", match[-1], user,
             "photo-194020282_457239099").send_message()


@bp.on.chat_message(regex=(r"(?i)((по)?трогать)\s*(.*)?"))
async def touch(message: Message, match, user: User):
    await Rp(message, "потрогал", match[-1], user,
             "photo-194020282_457239105").send_message()


@bp.on.chat_message(regex=(r"(?i)(насрать|обо(сс|с)рать)\s*(.*)?"))
async def give_a_shit(message: Message, match, user: User):
    await Rp(message, "насрал", match[-1], user,
             "photo-194020282_457239088").send_message()


@bp.on.chat_message(regex=(r"(?i)(навонять)\s*(.*)?"))
async def stink(message: Message, match, user: User):
    await Rp(message, "навонял", match[-1], user,
             "photo-194020282_457239087", Case.DATIVE).send_message()


@bp.on.chat_message(regex=(r"(?i)((по)?лапать)\s*(.*)?"))
async def paw(message: Message, match, user: User):
    await Rp(message, "полапал", match[-1], user,
             "photo-194020282_457239102").send_message()


@bp.on.chat_message(regex=(r"(?i)(съесть)\s*(.*)?"))
async def eat(message: Message, match, user: User):
    await Rp(message, "съел", match[-1], user,
             "photo-194020282_457239108").send_message()


@bp.on.chat_message(regex=(r"(?i)(откусить)\s*(.*)?"))
async def take_a_bite(message: Message, match, user: User):
    await Rp(message, "откусил", match[-1], user,
             "photo-194020282_457239095").send_message()


@bp.on.chat_message(regex=(r"(?i)(укусить)\s*(.*)?"))
async def bite(message: Message, match, user: User):
    await Rp(message, "укусил", match[-1], user,
             "photo-194020282_457239115").send_message()


@bp.on.chat_message(regex=(r"(?i)(поцеловать)\s*(.*)?"))
async def kiss(message: Message, match, user: User):
    await Rp(message, "поцеловал", match[-1], user,
             "photo-194020282_457239106").send_message()


@bp.on.chat_message(regex=(r"(?i)(напасть)\s*(.*)?"))
async def attack(message: Message, match, user: User):
    await Rp(message, "напал на", match[-1], user,
             "photo-194020282_457239116").send_message()


@bp.on.chat_message(regex=(r"(?i)(разрезать)\s*(.*)?"))
async def cut(message: Message, match, user: User):
    await Rp(message, "разрезал", match[-1], user,
             "photo-194020282_457239119").send_message()


@bp.on.chat_message(regex=(r"(?i)(ра(с|сс)трелять)\s*(.*)?"))
async def shoot(message: Message, match, user: User):
    await Rp(message, "расстрелял", match[-1], user,
             "photo-194020282_457239120").send_message()


@bp.on.chat_message(regex=(r"(?i)(помацать)\s*(.*)?"))
async def pomat(message: Message, match, user: User):
    await Rp(message, "помацал", match[-1], user,
             "photo-194020282_457239118").send_message()


@bp.on.chat_message(regex=(r"(?i)(захуярить)\s*(.*)?"))
async def fuck_up(message: Message, match, user: User):
    await Rp(message, "захуярил", match[-1], user,
             "photo-194020282_457239117").send_message()


class Rp():
    '''
    Класс для лёгкого создания РП хендлеров
    '''

    def __init__(
            self, message: Message, word: str, item: str, from_user: User,
            image=None, case: Case | None = Case.ACCUSATIVE) -> None:
        self.message = message

        self.word = " ".join((word, item))
        self.from_user = from_user
        self.image = image
        self.case = case

    async def get_text(self) -> str:
        self.to_user = await User.get(
            id=self.message.reply_message.from_id,  # type: ignore
            chat_id=self.message.peer_id)

        return (f"{await get_mention(self.from_user)} {self.word} "
                f"{await get_mention(self.to_user, self.case)}")

    async def send_message(self) -> None:
        setting = await Setting.get(chat_id=self.message.peer_id,
                                    id=2)
        if not setting.value:
            self.image = None
        await self.message.answer(await self.get_text(),
                                  attachment=self.image,
                                  disable_mentions=True)
