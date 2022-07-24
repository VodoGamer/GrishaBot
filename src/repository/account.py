from pymorphy2 import MorphAnalyzer
from vkbottle.bot import Blueprint

from db.new_models import User, UserNameCases

morph = MorphAnalyzer()
bp = Blueprint("user_repository")


async def get_user_name(user: User,
                        case: UserNameCases = UserNameCases.NOM):
    if user.id < 0:
        return (await bp.api.groups.get_by_id([user.id]))[0].name
    elif not user.custom_name:
        return (await bp.api.users.get(user_id=user.id,
                                       name_case=case.value[1]))[0].first_name
    raw_name = morph.parse(user.custom_name)[0]
    return raw_name.inflect(  # type: ignore
        {case.value[0]}).word.capitalize()


async def get_user_mention(user: User,
                           case: UserNameCases = UserNameCases.NOM):
    modificator = "id" if user.id > 0 else "club"
    user_id = abs(user.id)
    return f"@{modificator}{user_id} ({await get_user_name(user, case)})"
