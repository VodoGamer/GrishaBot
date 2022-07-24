from datetime import datetime
from enum import Enum

from tortoise import fields
from tortoise.models import Model


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
    id: int = fields.IntField(pk=True, generated=False)
    owner_id: int = fields.IntField(null=True)
    messages_count: int = fields.IntField(default=1)
    last_person_of_day_use: datetime = fields.DatetimeField(null=True)


class User(Model):
    id: int = fields.IntField(pk=True, generated=False)
    chat = fields.ForeignKeyField('models.Chat', related_name='users')
    is_admin: bool = fields.BooleanField(default=False)  # type: ignore
    custom_name: str = fields.CharField(max_length=255, null=True)
    messages_count: int = fields.IntField(default=1)
    sex_request: int = fields.IntField(null=True)

    # Money
    money: int = fields.IntField(default=0)
    last_bonus_use: datetime = fields.DatetimeField(null=True)

    # Dick
    dick_size: int = fields.IntField(default=0)
    last_dick_growth_use: datetime = fields.DatetimeField(null=True)

    # Casino
    casino_bet_amount: int = fields.IntField(null=True)
    casino_bet_color: SmileyCasinoChips = fields.CharEnumField(
        SmileyCasinoChips,
        max_length=5,
        null=True)


class Setting(Model):
    id: int = fields.IntField(pk=True, generated=False)
    chat = fields.ForeignKeyField('models.Chat', related_name='settings')
    title: str = fields.CharField(max_length=255)
    value: int = fields.IntField()
    max_value: int = fields.IntField(default=1)
