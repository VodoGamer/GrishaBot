from datetime import datetime, timedelta
from enum import Enum
from random import choice

from pytz import UTC
from vkbottle.bot import Blueprint, Message

from src.db.models import Setting, User
from src.repository.account import get_mention, is_command_available

bp = Blueprint("coin_game")
bp.labeler.vbml_ignore_case = True


class CoinSides(Enum):
    EAGLE = "орёл"
    TAILS = "решка"


def choice_coin_side() -> CoinSides:
    return choice(list(CoinSides))


@bp.on.chat_message(text="монетка <(орёл|решка)*bet_side> <bet:int>")
async def coin_game_with_set_side(message: Message, user: User,
                                  bet_side: list[str], bet: int):
    await the_coin_game(message, user, CoinSides(bet_side[0]), int(bet))


async def the_coin_game(
        message: Message,
        user: User,
        bet_side: CoinSides,
        bet_amount: int):
    if user.money < bet_amount:
        if (await Setting.get(chat_id=message.peer_id, id=5)).value:
            await message.answer(sticker_id=35)
        await message.reply("Недостаточно денег!")
        return
    user.money -= bet_amount

    cooldown = is_command_available(user.last_coin_game,
                                    timedelta(minutes=5))
    if cooldown:
        await message.reply(
            f"Следущая игра в монетку будет доступна через: {cooldown}")
        return

    win_side = choice_coin_side()
    await message.reply(f"Выпало: {win_side.value}")

    if win_side == bet_side:
        user.money += bet_amount * 2
        word = "выиграл"
    else:
        word = "проиграл"

    user.last_coin_game = datetime.now(tz=UTC)
    await user.save()
    await message.answer(f"{await get_mention(user)} {word} {bet_amount} "
                         "в монетке",
                         disable_mentions=True)
