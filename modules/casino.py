from datetime import datetime, timedelta
import asyncio

from vkbottle.bot import Blueprint, Message

from modules.models import User, Casino, CasinoUser, Settings


bp = Blueprint("Casino")


@bp.on.chat_message(regex=(r"(?i)^(\d*)\s*?(к|ч|з)$"))
async def new_bet(message: Message, match):
    settings = Settings(message.peer_id)
    if (await settings.get_value("casino"))[0] == "False":
        await message.reply("❌| Казино выключено в настройках этого чата!\n"
                            "Попроси администраторов его включить")
        return
    user = User(message.peer_id, message.from_id)
    await user.init()
    casino_user = CasinoUser(message.peer_id, message.from_id)
    await casino_user.init()
    if int(match[0]) <= 0:
        await message.reply("❌| Иди нахуй!")
        return
    if user.money >= int(match[0]):  # Проверка баланса
        casino_user_check = await casino_user.check()
        if not casino_user_check:  # Не учавствует ли уже юзер
            await casino_user.register_bet(
                int(match[0]),
                await convert_text_to_emoji(match[1]))

            await user.change_money(-int(match[0]))
            await message.reply("Ставка защитана!")
        else:
            await message.reply(f"Вы уже поставили {casino_user_check[2]} "
                                f"на {casino_user_check[3]}")
    else:
        await message.reply("У вас недостаточно денег!")


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*го$"))
async def twist(message: Message):
    settings = Settings(message.peer_id)
    if (await settings.get_value("casino"))[0] == "False":
        await message.reply("❌| Казино выключено в настройках этого чата!\n"
                            "Попроси администраторов его включить")
        return

    casino = Casino(message.peer_id)
    casino_users = await casino.get_users()
    if not await casino.get_last_go():
        now = datetime.now()
        db_time = int((await settings.get_value("casino_cooldown"))[0])
        last_go = datetime.strptime(await casino.get_last_go(), "%H:%M:%S.%f")
        next_time = last_go + timedelta(seconds=db_time)

        if next_time.time() > now.time():
            await message.answer("Следующую крутку можно будет начать "
                                 f"в\n{str(next_time.time()).split('.')[0]}"
                                 " по мск")
            return
    if casino_users == []:
        await message.reply("❌| Никто не учавствует в казино!")
        return

    casino_users_mentions = []
    for casino_user in casino_users:
        user = User(message.peer_id, casino_user[1])
        await user.init()
        casino_users_mentions.append(await user.get_mention())

    await message.answer("В казино учавствуют:\n"
                         "{}".format('\n'.join(casino_users_mentions)),
                         disable_mentions=True)

    winner_feature = await casino.get_winner_feature()
    winner_users = await casino.get_winner_users(winner_feature)
    winner_users_mention = []

    for winner_user in winner_users:
        winner_user = User(message.peer_id, winner_user)
        await winner_user.init()
        winner_casino_user = CasinoUser(message.peer_id, winner_user.user_id)
        await winner_casino_user.init()
        if winner_feature != "🍀":
            winner_cash = winner_casino_user.bet * 2
        else:
            winner_cash = winner_casino_user.bet * 8

        await winner_user.change_money(winner_cash)
        winner_users_mention.append(f"{await winner_user.get_mention()} "
                                    f"выиграл {winner_cash} 💵")

    await casino.delete_all()

    await message.answer("🎲| Бросаем кубики",
                         "video-194020282_456239019")
    await asyncio.sleep(3)
    if winner_users_mention == []:
        await message.answer(f"Выпало {winner_feature}.\nНикто не выиграл.")
    else:
        await message.answer(f"Выпало {winner_feature}.\n"
                             "{}".format('\n'.join(winner_users_mention)),
                             disable_mentions=True)
    await casino.add_to_history(winner_feature)  # Добавление в историю / лог


@bp.on.chat_message(regex=(r"(?i)^(!|\.|\/)?\s*лог|история$"))
async def get_log(message: Message):
    casino = Casino(message.peer_id)
    history = await casino.get_history()
    if history is None:
        await message.reply("За сегодня ещё никто не играл!")
        return
    await message.reply("🕓| Предыдущие крутки за сегодня:\n"
                        "{}".format("\n".join(history)),
                        disable_mentions=True)


async def convert_text_to_emoji(text: str):
    if text.lower() == "к":
        return "🔴"
    elif text.lower() == "ч":
        return "⚫️"
    elif text.lower() == "з":
        return "🍀"
