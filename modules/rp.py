from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import RegexRule, ReplyMessageRule
import modules.models as models

bp = Blueprint("Rp commands")
bp.labeler.auto_rules = [ReplyMessageRule()]


@bp.on.chat_message(RegexRule("(ударить|ёбнуть) (.*)|ударить|ёбнуть"))
async def kick(message: Message, match):
    await Rp(message, "ударил", match[1], "photo-194020282_457239111").send_message()


@bp.on.chat_message(RegexRule("(обдристать) (.*)|обдристать"))
async def poooooo(message: Message, match):
    await Rp(message, "обдристал", match[1], "photo-194020282_457239089").send_message()


@bp.on.chat_message(RegexRule("(выебать|трахнуть) (.*)|выебать|трахнуть"))
async def fuck(message: Message, match):
    await Rp(message, "выебал", match[1], "photo-194020282_457239085").send_message()


@bp.on.chat_message(RegexRule("(уебать) (.*)|уебать"))
async def fuck(message: Message, match):
    await Rp(message, "уебал", match[1], "photo-194020282_457239112").send_message()


@bp.on.chat_message(RegexRule("(кончить) (.*)|кончить"))
async def fuck(message: Message, match):
    await Rp(message, "обкончал", match[1], "photo-194020282_457239090").send_message()


@bp.on.chat_message(RegexRule("(отсосать) (.*)|отсосать"))
async def fuck(message: Message, match):
    await Rp(message, "отсосал у", match[1], "photo-194020282_457239097").send_message()


@bp.on.chat_message(RegexRule("(обнять|прижать) (.*)|обнять|прижать"))
async def fuck(message: Message, match):
    await Rp(message, "обнял", match[1], "photo-194020282_457239092").send_message()


@bp.on.chat_message(RegexRule("(засосать) (.*)|засосать"))
async def fuck(message: Message, match):
    await Rp(message, "засосал", match[1], "photo-194020282_457239086").send_message()


@bp.on.chat_message(RegexRule("(п.рнуть) (.*)|п.рнуть"))
async def fuck(message: Message, match):
    await Rp(message, "пёрнул на", match[1], "photo-194020282_457239098").send_message()


@bp.on.chat_message(RegexRule("(о(т|тт)рахать) (.*)|о(т|тт)рахать"))
async def fuck(message: Message, match):
    await Rp(message, "обтрахал", match[-2], "photo-194020282_457239094").send_message()


@bp.on.chat_message(RegexRule("(убить) (.*)|убить"))
async def fuck(message: Message, match):
    await Rp(message, "убил", match[1], "photo-194020282_457239110").send_message()


@bp.on.chat_message(RegexRule("(послать) (.*)|послать"))
async def fuck(message: Message, match):
    await Rp(message, "послал", match[1], "photo-194020282_457239104").send_message()


@bp.on.chat_message(RegexRule("(шлёпнуть) (.*)|шлёпнуть"))
async def fuck(message: Message, match):
    await Rp(message, "шлёпнул", match[1], "photo-194020282_457239113").send_message()


@bp.on.chat_message(RegexRule("(пнуть) (.*)|пнуть"))
async def fuck(message: Message, match):
    await Rp(message, "пнул", match[1], "photo-194020282_457239100").send_message()


@bp.on.chat_message(RegexRule("(сжечь) (.*)|сжечь"))
async def fuck(message: Message, match):
    await Rp(message, "сжёг", match[1], "photo-194020282_457239107").send_message()


@bp.on.chat_message(RegexRule("(понюхать) (.*)|понюхать"))
async def fuck(message: Message, match):
    await Rp(message, "понюхал", match[1], "photo-194020282_457239103").send_message()


@bp.on.chat_message(RegexRule("(лизнуть|полизать|облизать) (.*)|(лизнуть|полизать|облизать)"))
async def fuck(message: Message, match):
    await Rp(message, "облизал", match[-2], "photo-194020282_457239091").send_message()


@bp.on.chat_message(RegexRule("(отлизать) (.*)|отлизать"))
async def fuck(message: Message, match):
    await Rp(message, "отлизал", match[1], "photo-194020282_457239096", "gent").send_message()


@bp.on.chat_message(RegexRule("(погладить) (.*)|погладить"))
async def fuck(message: Message, match):
    await Rp(message, "погладил", match[1], "photo-194020282_457239101").send_message()


@bp.on.chat_message(RegexRule("(обоссать|обосать) (.*)|обоссать|обосать"))
async def fuck(message: Message, match):
    await Rp(message, "обоссал", match[1], "photo-194020282_457239093").send_message()


@bp.on.chat_message(RegexRule("(плюнуть) (.*)|плюнуть"))
async def fuck(message: Message, match):
    await Rp(message, "плюнул", match[1], "photo-194020282_457239099").send_message()


@bp.on.chat_message(RegexRule("(потрогать|трогать) (.*)|потрогать|трогать"))
async def fuck(message: Message, match):
    await Rp(message, "потрогал", match[1], "photo-194020282_457239105").send_message()


@bp.on.chat_message(RegexRule("(насрать|обосрать) (.*)|насрать|обосрать"))
async def fuck(message: Message, match):
    await Rp(message, "насрал", match[1], "photo-194020282_457239088").send_message()


@bp.on.chat_message(RegexRule("(навонять) (.*)|навонять"))
async def fuck(message: Message, match):
    await Rp(message, "навонял", match[1], "photo-194020282_457239087", "datv").send_message()


@bp.on.chat_message(RegexRule("(полапать|лапать) (.*)|полапать|лапать"))
async def fuck(message: Message, match):
    await Rp(message, "полапал", match[1], "photo-194020282_457239102").send_message()


@bp.on.chat_message(RegexRule("(съесть) (.*)|съесть"))
async def fuck(message: Message, match):
    await Rp(message, "съел", match[1], "photo-194020282_457239108").send_message()


@bp.on.chat_message(RegexRule("(откусить) (.*)|откусить"))
async def fuck(message: Message, match):
    await Rp(message, "откусил", match[1], "photo-194020282_457239095").send_message()


@bp.on.chat_message(RegexRule("(укусить) (.*)|укусить"))
async def fuck(message: Message, match):
    await Rp(message, "укусил", match[1], "photo-194020282_457239115").send_message()


@bp.on.chat_message(RegexRule("(поцеловать) (.*)|поцеловать"))
async def fuck(message: Message, match):
    await Rp(message, "поцеловал", match[1], "photo-194020282_457239106").send_message()


@bp.on.chat_message(RegexRule("(напасть) (.*)|напасть"))
async def fuck(message: Message, match):
    await Rp(message, "напал на", match[1], "photo-194020282_457239116").send_message()


class Rp():
    '''
    Класс для лёгкого создания РП хендлеров
    '''

    def __init__(self, message: Message, word: str, item: str,
                 image=None, case="accs") -> None:
        self.message = message
        self.from_user = models.User(message.peer_id, message.from_id)
        self.to_user = models.User(message.peer_id,
                                   message.reply_message.from_id)

        self.word = word
        self.item = item
        self.image = image
        self.case = case

    async def get_text(self) -> str:
        if self.item != None: self.word = f"{self.word} {self.item}"
        return (f"{await self.from_user.get_mention()} {self.word} "
                f"{await self.to_user.get_mention(self.case)}")

    async def send_message(self) -> None:
        settings = models.Settings(self.from_user.chat_id)
        if settings.get_value("pictures")[0] == "True":
            await self.message.answer(await self.get_text(),
                                      attachment=self.image)
        else:
            await self.message.answer(await self.get_text())
