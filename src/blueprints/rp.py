from vkbottle.bot import Blueprint, Message

from src.db.models import User
from src.repository.account import Case, get_mention
from src.rules.mention import HasUserMention

bp = Blueprint("Rp commands")


@bp.on.chat_message(HasUserMention(("ударить", "уебать")))
async def to_kick(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "ударил", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("обдристать"))
async def poooooo(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "обдристал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention(("выебать", "трахнуть")))
async def fuck(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "выебал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("уебать"))
async def to_fuck_off(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "уебал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("кончить"))
async def cum(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "обкончал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("отсосать"))
async def suck_it(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "отсосал у", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention(("обнять", "прижать")))
async def hug(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "обнял", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("засосать"))
async def suck(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "засосал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("пёрнуть"))
async def fart(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "пёрнул на", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("оттрахать"))
async def fuck_strong(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "обтрахал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("убить"))
async def kill(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "убил", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("послать"))
async def fuck_off(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "послал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("шлёпнуть"))
async def slap(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "шлёпнул", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("пнуть"))
async def kick(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "пнул", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("сжечь"))
async def burn(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "сжёг", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("понюхать"))
async def smell_it(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "понюхал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention(("лизнуть", "полизать", "облизать")))
async def lick(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "облизал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("отлизать"))
async def lick_it_off(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "отлизал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("погладить"))
async def stroke(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "погладил", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention(("обоссать", "обосать")))
async def piss_on(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "обоссал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("плюнуть"))
async def spit(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "плюнул в", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention(("потрогать", "трогать")))
async def touch(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "потрогал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("насрать"))
async def give_a_shit(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "насрал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("навонять"))
async def stink(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "навонял", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("полапать"))
async def paw(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "полапал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("съесть"))
async def eat(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "съел", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("откусить"))
async def take_a_bite(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "откусил", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("укусить"))
async def bite(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "укусил", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("поцеловать"))
async def kiss(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "поцеловал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("напасть"))
async def attack(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "напал на", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("разрезать"))
async def cut(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "разрезал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("расстрелять"))
async def shoot(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "расстрелял", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("помацать"))
async def pomat(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "помацал", action, user, user_id).send_message()


@bp.on.chat_message(HasUserMention("захуярить"))
async def fuck_up(message: Message, action: str, user_id: int, user: User):
    await Rp(message, "захуярил", action, user, user_id).send_message()


class Rp:
    """
    Класс для лёгкого создания РП хендлеров
    """

    def __init__(
        self,
        message: Message,
        command: str,
        action: str,
        from_user: User,
        to_id: int,
        image=None,
        case: Case | None = Case.ACCUSATIVE,
    ) -> None:
        self.message = message

        self.command = " ".join((command, action))
        self.from_user = from_user
        self.to_id = to_id
        self.image = image
        self.case = case

    async def get_text(self) -> str:
        self.to_user = await User.get(uid=self.to_id, chat_id=self.message.peer_id)

        return (
            f"{await get_mention(self.from_user)} {self.command} "
            f"{await get_mention(self.to_user, self.case)}"
        )

    async def send_message(self) -> None:
        await self.message.answer(
            await self.get_text(), attachment=self.image, disable_mentions=True
        )
