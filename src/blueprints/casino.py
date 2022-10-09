import asyncio
from datetime import datetime, timedelta
from random import choice, randint

from pytz import UTC
from vkbottle.bot import Blueprint, Message

from src.bot.phrases import not_enough_money, setting_has_disabled
from src.db.models import Casino, CasinoChips, Chat, Setting, User
from src.repository.account import get_mention, is_command_available

bp = Blueprint("Casino")


@bp.on.chat_message(regex=(r"(?i)^\.*\s*(\d*)\s*(к|ч|з)$"))
async def new_bet(message: Message, match, user: User, chat: Chat):
    bet = int(match[0])

    if not (await Setting.get(cid=2, chat=chat)).value:
        await message.reply(setting_has_disabled.format(thing="Казино выключено"))
        return

    if bet <= 0:
        await message.reply("❌| Иди нахуй!")
        return

    if user.money < bet:  # Проверка баланса
        await message.reply(not_enough_money)
        return

    if user.casino_bet_color is not None:
        # Не учавствует ли уже юзер
        await message.reply(
            f"У тебя уже есть ставка:\n {user.casino_bet_amount} "
            f"на {user.casino_bet_color.value}"
        )
        return

    user.casino_bet_amount = bet
    user.money -= bet
    user.casino_bet_color = convert_text_to_emoji(match[1])
    await user.save()

    await message.reply("Ставка сделана!🎲")


@bp.on.chat_message(regex=(r"(?i)^\.*\s*го$"))
async def twist(message: Message, chat: Chat):
    setting = await Setting.get(cid=2, chat=chat)
    if not setting.value:
        await message.reply(setting_has_disabled.format(thing="Казино выключено"))
        return

    cooldown_setting = await Setting.get(cid=3, chat=chat)
    cooldown = is_command_available(chat.last_casino, timedelta(seconds=cooldown_setting.value))

    if not cooldown[0]:
        await message.reply(f"❌ | Следующую крутку можно будет сделать через {cooldown[1]}")
        return

    chat.last_casino = datetime.now(tz=UTC)
    await chat.save()

    casino_users = await User.filter(chat=chat).exclude(casino_bet_color=None)
    if casino_users == []:
        await message.reply("❌| Никто не учавствует в казино!")
        return

    casino_users_mentions = [await get_mention(casino_user) for casino_user in casino_users]

    await message.answer(
        "В казино учавствуют:\n{}".format("\n".join(casino_users_mentions)),
        disable_mentions=True,
    )

    if randint(1, 26) == 1:
        winner_feature = CasinoChips.GREEN
        winner_ratio = 8
    else:
        winner_feature = choice((CasinoChips.RED, CasinoChips.BLACK))
        winner_ratio = 2
    winner_users = await User.filter(chat=chat, casino_bet_color=winner_feature)

    winner_users_mention = []
    for winner_user in winner_users:
        winner_cash = winner_user.casino_bet_amount * winner_ratio
        winner_user.money += winner_cash + winner_user.casino_bet_amount
        await winner_user.save()

        winner_users_mention.append(f"{await get_mention(winner_user)} выиграл {winner_cash} 💵")

    await message.answer("🎲| Бросаем кубики", "video-194020282_456239019")
    await asyncio.sleep(2)

    for casino_user in casino_users:
        casino_user.casino_bet_amount = 0
        casino_user.casino_bet_color = None
        await casino_user.save(update_fields=("casino_bet_amount", "casino_bet_color"))

    if winner_users_mention == []:
        await message.answer(f"Выпало {winner_feature.value}.\nНикто не выиграл.")
    else:
        await message.answer(
            f"Выпало {winner_feature.value}.\n" "{}".format("\n".join(winner_users_mention)),
            disable_mentions=True,
        )
    await Casino.create(chat=chat, winner_feature=winner_feature)


@bp.on.chat_message(regex=(r"(?i)^\.*\s*лог|история$"))
async def get_log(message: Message, chat: Chat):
    casinos = await Casino.filter(chat=chat).order_by("id").limit(10)
    if casinos == []:
        await message.reply("За сегодня ещё никто не играл!")
        return
    history = "\n".join(casino.winner_feature.value for casino in casinos)
    await message.reply(f"🕓| Предыдущие крутки за сегодня:\n {history}", disable_mentions=True)


def convert_text_to_emoji(text: str):
    if text.lower() == "к":
        return CasinoChips.RED
    elif text.lower() == "ч":
        return CasinoChips.BLACK
    elif text.lower() == "з":
        return CasinoChips.GREEN
