from datetime import datetime, timedelta
from enum import Enum

from pytrovich.enums import Case, Gender, NamePart
from pytrovich.maker import PetrovichDeclinationMaker
from pytz import UTC
from vkbottle.bot import Blueprint

from src.db.models import User

maker = PetrovichDeclinationMaker()
bp = Blueprint("user_repository")


class TopType(Enum):
    money = 0
    dicks = 1


async def get_name(user: User,
                   case: Case | None = None,
                   gender: Gender = Gender.MALE):
    if user.id < 0:
        name = (await bp.api.groups.get_by_id([user.id]))[0].name
    elif not user.custom_name:
        name = (await bp.api.users.get(user_id=user.id))[0].first_name
    else:
        name = user.custom_name

    if case is None:
        return name
    else:
        return maker.make(
            NamePart.FIRSTNAME,
            gender,
            case,
            name)  # type: ignore


async def get_mention(user: User,
                      case: Case | None = None,
                      gender: Gender = Gender.MALE):
    modificator = "id" if user.id > 0 else "club"
    user_id = abs(user.id)
    return f"@{modificator}{user_id} ({await get_name(user, case, gender)})"


def command_not_available(last_use_command: datetime | None,
                          delta: timedelta) -> bool | str:
    '''Проверяет можно ли использовать команду, на которой есть кд'''
    if last_use_command:
        now = datetime.now(tz=UTC)
        db_date_delta = last_use_command + delta
        if db_date_delta > now:
            return str(db_date_delta - now).split('.')[0]
    return False


async def get_top_list(users_list: list[User],
                       top_type: TopType) -> str | bool:
    '''получение топа пользователей по параметру'''
    if users_list:
        users_mentions = []

        for user in users_list:
            if top_type == TopType.money:
                end_phrase = f"{user.money} 💵"
            elif top_type == TopType.dicks:
                end_phrase = f"{user.dick_size}"
            else:
                raise ValueError("top_type unbound")

            users_mentions.append(
                f"{await get_mention(user)} | {end_phrase}")
        return "\n".join(users_mentions)
    else:
        return False
