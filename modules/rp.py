from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import ReplyMessageRule

from modules.models import User, Settings


bp = Blueprint("Rp commands")
bp.labeler.auto_rules = [ReplyMessageRule()]


@bp.on.chat_message(regex=(r"(?i)(ударить|ёбнуть)\s*(.*)?"))
async def kick(message: Message, match):
    await Rp(message, "ударил", match[-1],
             "photo-194020282_457239111").send_message()


@bp.on.chat_message(regex=(r"(?i)(обдристать)\s*(.*)?"))
async def poooooo(message: Message, match):
    await Rp(message, "обдристал", match[-1],
             "photo-194020282_457239089").send_message()


@bp.on.chat_message(regex=(r"(?i)(выебать|трахнуть)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "выебал", match[-1],
             "photo-194020282_457239085").send_message()


@bp.on.chat_message(regex=(r"(?i)(уебать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "уебал", match[-1],
             "photo-194020282_457239112").send_message()


@bp.on.chat_message(regex=(r"(?i)(кончить)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "обкончал", match[-1],
             "photo-194020282_457239090").send_message()


@bp.on.chat_message(regex=(r"(?i)(отсосать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "отсосал у", match[-1],
             "photo-194020282_457239097").send_message()


@bp.on.chat_message(regex=(r"(?i)(обнять|прижать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "обнял", match[-1],
             "photo-194020282_457239092").send_message()


@bp.on.chat_message(regex=(r"(?i)(засосать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "засосал", match[-1],
             "photo-194020282_457239086").send_message()


@bp.on.chat_message(regex=(r"(?i)(п.рнуть)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "пёрнул на", match[-1],
             "photo-194020282_457239098").send_message()


@bp.on.chat_message(regex=(r"(?i)(о(т|тт)рахать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "обтрахал", match[-1],
             "photo-194020282_457239094").send_message()


@bp.on.chat_message(regex=(r"(?i)(убить)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "убил", match[-1],
             "photo-194020282_457239110").send_message()


@bp.on.chat_message(regex=(r"(?i)(послать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "послал", match[-1],
             "photo-194020282_457239104").send_message()


@bp.on.chat_message(regex=(r"(?i)(шлёпнуть)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "шлёпнул", match[-1],
             "photo-194020282_457239113").send_message()


@bp.on.chat_message(regex=(r"(?i)(пнуть)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "пнул", match[-1],
             "photo-194020282_457239100").send_message()


@bp.on.chat_message(regex=(r"(?i)(сжечь)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "сжёг", match[-1],
             "photo-194020282_457239107").send_message()


@bp.on.chat_message(regex=(r"(?i)(понюхать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "понюхал", match[-1],
             "photo-194020282_457239103").send_message()


@bp.on.chat_message(regex=(r"(?i)(лизнуть|облизать|полизать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "облизал", match[-1],
             "photo-194020282_457239091").send_message()


@bp.on.chat_message(regex=(r"(?i)(отлизать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "отлизал", match[-1],
             "photo-194020282_457239096", "gent").send_message()


@bp.on.chat_message(regex=(r"(?i)(погладить)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "погладил", match[-1],
             "photo-194020282_457239101").send_message()


@bp.on.chat_message(regex=(r"(?i)(обо(с|сс)ать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "обоссал", match[-1],
             "photo-194020282_457239093").send_message()


@bp.on.chat_message(regex=(r"(?i)(плюнуть)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "плюнул в", match[-1],
             "photo-194020282_457239099").send_message()


@bp.on.chat_message(regex=(r"(?i)((по)?трогать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "потрогал", match[-1],
             "photo-194020282_457239105").send_message()


@bp.on.chat_message(regex=(r"(?i)(насрать|обо(сс|с)рать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "насрал", match[-1],
             "photo-194020282_457239088").send_message()


@bp.on.chat_message(regex=(r"(?i)(навонять)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "навонял", match[-1],
             "photo-194020282_457239087", "datv").send_message()


@bp.on.chat_message(regex=(r"(?i)((по)?лапать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "полапал", match[-1],
             "photo-194020282_457239102").send_message()


@bp.on.chat_message(regex=(r"(?i)(съесть)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "съел", match[-1],
             "photo-194020282_457239108").send_message()


@bp.on.chat_message(regex=(r"(?i)(откусить)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "откусил", match[-1],
             "photo-194020282_457239095").send_message()


@bp.on.chat_message(regex=(r"(?i)(укусить)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "укусил", match[-1],
             "photo-194020282_457239115").send_message()


@bp.on.chat_message(regex=(r"(?i)(поцеловать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "поцеловал", match[-1],
             "photo-194020282_457239106").send_message()


@bp.on.chat_message(regex=(r"(?i)(напасть)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "напал на", match[-1],
             "photo-194020282_457239116").send_message()


@bp.on.chat_message(regex=(r"(?i)(разрезать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "разрезал", match[-1],
             "photo-194020282_457239119").send_message()


@bp.on.chat_message(regex=(r"(?i)(ра(с|сс)трелять)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "расстрелял", match[-1],
             "photo-194020282_457239120").send_message()


@bp.on.chat_message(regex=(r"(?i)(помацать)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "помацал", match[-1],
             "photo-194020282_457239118").send_message()


@bp.on.chat_message(regex=(r"(?i)(захуярить)\s*(.*)?"))
async def fuck(message: Message, match):
    await Rp(message, "захуярил", match[-1],
             "photo-194020282_457239117").send_message()


class Rp():
    '''
    Класс для лёгкого создания РП хендлеров
    '''

    def __init__(self, message: Message, word: str, item: str,
                 image=None, case="accs") -> None:
        self.message = message
        self.from_user = User(message.peer_id, message.from_id)
        self.to_user = User(message.peer_id,
                            message.reply_message.from_id)

        self.word = word
        self.item = item
        self.image = image
        self.case = case

    async def get_text(self) -> str:
        if self.item is not None:
            self.word = f"{self.word} {self.item}"
        return (f"{await self.from_user.get_mention()} {self.word} "
                f"{await self.to_user.get_mention(self.case)}")

    async def send_message(self) -> None:
        settings = Settings(self.from_user.chat_id)
        if settings.get_value("pictures")[0] == "True":
            await self.message.answer(await self.get_text(),
                                      attachment=self.image,
                                      disable_mentions=True)
        else:
            await self.message.answer(await self.get_text(),
                                      disable_mentions=True)
