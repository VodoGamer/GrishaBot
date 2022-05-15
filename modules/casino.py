import asyncio
from vkbottle.bot import Blueprint, Message
from modules.models import User, Casino, CasinoUser, Settings


bp = Blueprint("Casino")


@bp.on.chat_message(regex=("(?i)^(\d*)\s*?(к|ч|з)$"))
async def new_bet(message: Message, match):
    settings = Settings(message.peer_id)
    if settings.get_value("casino")[0] == "False":
        await message.reply("Казино выключено в настройках этого чата!")
        return
    user = User(message.peer_id, message.from_id)
    casino_user = CasinoUser(message.peer_id, message.from_id)
    if int(match[0]) <= 0:
        await message.reply("Иди нахуй!")
        return
    if user.money >= int(match[0]):  # Проверка баланса
        casino_user_check = casino_user.check()
        if not casino_user_check:  # Не учавствует ли уже юзер
            casino_user.register_bet(
                int(match[0]),
                await convert_text_to_emoji(match[1]))

            user.change_money(-int(match[0]))
            await message.reply("Ставка защитана!")
        else:
            await message.reply(f"Вы уже поставили {casino_user_check[2]} "
                                f"на {casino_user_check[3]}")
    else:
        await message.reply("У вас недостаточно денег!")


@bp.on.chat_message(regex=("(?i)^го$"))
async def twist(message: Message):
    settings = Settings(message.peer_id)
    if settings.get_value("casino")[0] == "False":
        await message.reply("Казино выключено в настройках этого чата!")
        return
    casino = Casino(message.peer_id)
    casino_users = casino.get_users()
    casino_money = casino.get_all_money()
    if casino_users == []:
        await message.reply("Никто не учавствует в казино!")
        return

    casino_users_mentions = []
    for casino_user in casino_users:
        casino_users_mentions.append(
            await User(message.peer_id, casino_user[1]).get_mention())

    await message.answer("В казино учавствуют:\n"
                         "{}".format('\n'.join(casino_users_mentions)))

    winner_feature = casino.get_winner_feature()
    winner_users = casino.get_winner_users(winner_feature)
    if winner_users != []:
        winner_cash = round(casino_money / len(winner_users) * 1.1)

    winner_users_mention = []
    for winner_user in winner_users:
        winner_user = User(message.peer_id, winner_user)
        winner_users_mention.append(await winner_user.get_mention())
        winner_user.change_money(winner_cash)

    casino.delete_all()

    await message.answer("🎲| Бросаем кубики")
    await asyncio.sleep(3)
    if winner_users_mention == []:
        await message.answer(f"Выпало {winner_feature}.\nНикто не выиграл.")
        return
    await message.answer(f"Выпало {winner_feature}.\n"
                         "{}"
                         f"\nполучили {winner_cash}"
                         "".format('\n'.join(winner_users_mention)))


async def convert_text_to_emoji(text: str):
    if text.lower() == "к":
        return "🔴"
    elif text.lower() == "ч":
        return "⚫️"
    elif text.lower() == "з":
        return "🍀"
