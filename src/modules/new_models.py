from enum import Enum

from pymorphy2 import MorphAnalyzer
from tortoise import fields
from tortoise.models import Model
from vkbottle.bot import Blueprint

bp = Blueprint("new_models")
morph = MorphAnalyzer()


class SmileyCasinoChips(Enum):
    RED = "🔴"
    BLACK = "⚫️"
    GREEN = "🍀"


class UserNameCases(Enum):
    NOM = ["nomn", "nom"]  # Именительный
    GEN = ["gent", "gen"]  # Родительный
    DAT = ["datv", "dat"]  # Дательный
    ACC = ["accs", "acc"]  # Венительный
    INS = ["ablt", "ins"]  # Творительный
    ABL = ["loct", "abl"]  # Предложный


class Chat(Model):
    id = fields.IntField(pk=True, generated=False)
    owner_id = fields.IntField()
    messages_count = fields.IntField(default=1)
    last_person_of_day_use = fields.DatetimeField(null=True)


class User(Model):
    id = fields.IntField(pk=True, generated=False)
    chat = fields.ForeignKeyField('models.Chat', related_name='users')
    is_admin = fields.BooleanField(default=False)
    custom_name = fields.CharField(max_length=255, null=True)
    messages_count = fields.IntField(default=1)
    sex_request = fields.IntField(null=True)

    # Money
    money = fields.IntField(default=0)
    last_bonus_use = fields.DatetimeField(null=True)

    # Dick
    dick_size = fields.IntField(default=0)
    last_dick_growth_use = fields.DatetimeField(null=True)

    # Casino
    casino_bet_amount = fields.IntField(null=True)
    casino_bet_color = fields.CharEnumField(SmileyCasinoChips, max_length=5,
                                            null=True)


async def get_user_name(user: User,
                        case: UserNameCases = UserNameCases.NOM):
    if not user.custom_name:
        name = await bp.api.users.get(user_id=user.id,
                                      name_case=case.value[1])
        return name[0].first_name
    raw_name = morph.parse(user.custom_name)[0]
    return raw_name.inflect(  # type: ignore
        {case.value[0]}).word.capitalize()


async def get_user_mention(user: User,
                           case: UserNameCases = UserNameCases.NOM):
    return f"@id{user.id} ({await get_user_name(user, case)})"


class Setting(Model):
    id = fields.IntField(pk=True, generated=False)
    chat = fields.ForeignKeyField('models.Chat', related_name='settings')
    title = fields.CharField(max_length=255)
    value = fields.IntField()
