from src.repository import account

from . import (
    balance,
    casino,
    chat_invite,
    coin_game,
    custom_name,
    dick,
    how_long,
    image,
    insults,
    person_of_day,
    rp,
    russian_roulette,
    setting,
    sex,
    stats,
)

modules_list = (
    account.bp,
    balance.bp,
    casino.bp,
    custom_name.bp,
    dick.bp,
    how_long.bp,
    insults.bp,
    person_of_day.bp,
    setting.bp,
    stats.bp,
    sex.bp,
    coin_game.bp,
    rp.bp,
    chat_invite.bp,
    image.bp,
    russian_roulette.bp,
)
