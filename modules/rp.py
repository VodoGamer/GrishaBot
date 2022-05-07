from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import VBMLRule, RegexRule, ReplyMessageRule
import modules.models as models

bp = Blueprint("Rp commands")


@bp.on.chat_message(ReplyMessageRule(), (VBMLRule("ударить <item>") | RegexRule("ударить")))
async def kick(message: Message, item: str = None):
    await Rp(message, "ударил", item, "accs").send_message()


class Rp():
    '''
    Класс для лёгкого создания РП хендлеров
    '''
    def __init__(self, message: Message, word, item, case) -> None:
        self.message = message
        self.from_user = models.User(message.peer_id, message.from_id)
        self.to_user = models.User(message.peer_id, message.reply_message.from_id)

        self.case = case
        self.word = word
        self.item = item

    async def get_text(self) -> str:
        if self.item != None: self.word = f"{self.word} {self.item}"
        return f"{await self.from_user.get_mention()} {self.word} {await self.to_user.get_mention(self.case)}"

    async def send_message(self) -> None:
        await self.message.answer(await self.get_text())
