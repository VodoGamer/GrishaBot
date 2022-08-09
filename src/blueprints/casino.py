import asyncio
from datetime import datetime, timedelta
from random import choice, randint
from pytz import UTC

from vkbottle.bot import Blueprint, Message

from src.db.models import Casino, CasinoChips, Chat, Setting, User
from src.repository.account import command_not_available, get_mention

bp = Blueprint("Casino")


@bp.on.chat_message(regex=(r"(?i)^(\d*)\s*?(к|ч|з)$"))
async def new_bet(message: Message, match, user: User):
    bet = int(match[0])

    setting = await Setting.get(id=3, chat_id=message.peer_id)
    if not setting.value:
        await message.reply("❌| Казино выключено в настройках этого чата!\n"
                            "Попроси администраторов его включить")
        return

    if bet <= 0:
        await message.reply("❌| Иди нахуй!")
        return

    if user.money < bet:  # Проверка баланса
        await message.reply("У вас недостаточно денег!")
        return

    if user.casino_bet_color is not None:
        # Не учавствует ли уже юзер
        await message.reply(f"Вы уже поставили {user.casino_bet_amount} "
                            f"на {user.casino_bet_color.value}")
        return

    user.casino_bet_amount = bet
    user.money -= bet
    user.casino_bet_color = convert_text_to_emoji(match[1])
    await user.save()

    await message.reply("Ставка защитана!")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*го$"))
async def twist(message: Message, chat: Chat):
    setting = await Setting.get(id=3, chat_id=chat.id)
    if not setting.value:
        await message.reply("❌| Казино выключено в настройках этого чата!\n"
                            "Попроси администраторов его включить")
        return

    cooldown_setting = await Setting.get(id=4, chat_id=chat.id)
    cooldown = command_not_available(
        chat.last_casino_use, timedelta(seconds=cooldown_setting.value))

    if cooldown:
        await message.reply("❌ | Следующую крутку можно будет начать через "
                            f"{cooldown}"
                            )
        return

    chat.last_casino_use = datetime.now(tz=UTC)
    await chat.save()

    casino_users = await User.filter(chat_id=chat.id)\
        .exclude(casino_bet_color=None)
    if casino_users == []:
        await message.reply("❌| Никто не учавствует в казино!")
        return

    casino_users_mentions = []
    for casino_user in casino_users:
        casino_users_mentions.append(await get_mention(casino_user))

    await message.answer("В казино учавствуют:\n"
                         "{}".format('\n'.join(casino_users_mentions)),
                         disable_mentions=True)

    if randint(1, 26) == 1:
        winner_feature = CasinoChips.GREEN
    else:
        winner_feature = choice((CasinoChips.RED,
                                 CasinoChips.BLACK))
    winner_users = await User.filter(chat_id=chat.id,
                                     casino_bet_color=winner_feature)

    winner_users_mention = []

    if winner_feature != CasinoChips.GREEN:
        winner_ratio = 2
    else:
        winner_ratio = 8

    for winner_user in winner_users:
        winner_cash = winner_user.casino_bet_amount * winner_ratio
        winner_user.money += winner_cash + winner_user.casino_bet_amount
        await winner_user.save()

        winner_users_mention.append(f"{await get_mention(winner_user)} "
                                    f"выиграл {winner_cash} 💵")

    await message.answer("🎲| Бросаем кубики",
                         "video-194020282_456239019")
    await asyncio.sleep(2)

    for casino_user in casino_users:
        casino_user.casino_bet_amount = 0
        casino_user.casino_bet_color = None
        await casino_user.save(update_fields=("casino_bet_amount",
                                              "casino_bet_color"))

    if winner_users_mention == []:
        await message.answer(
            f"Выпало {winner_feature.value}.\nНикто не выиграл.")
    else:
        await message.answer(f"Выпало {winner_feature.value}.\n"
                             "{}".format('\n'.join(winner_users_mention)),
                             disable_mentions=True)
    await Casino.create(chat_id=chat.id, winner_feature=winner_feature)


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*лог|история$"))
async def get_log(message: Message, chat: Chat):
    casinos = await Casino.filter(chat_id=chat.id).order_by('id').limit(15)
    if casinos == []:
        await message.reply("За сегодня ещё никто не играл!")
        return
    history = []
    for casino in casinos:
        history.append(casino.winner_feature.value)
    history = "\n".join(history)
    await message.reply(f"🕓| Предыдущие крутки за сегодня:\n {history}",
                        disable_mentions=True)


def convert_text_to_emoji(text: str):
    if text.lower() == "к":
        return CasinoChips.RED
    elif text.lower() == "ч":
        return CasinoChips.BLACK
    elif text.lower() == "з":
        return CasinoChips.GREEN
