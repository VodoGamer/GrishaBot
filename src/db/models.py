'''all bot's models'''
from datetime import datetime
from enum import Enum, IntEnum

from tortoise import fields
from tortoise.models import Model


class CasinoChips(Enum):
    RED = "🔴"
    BLACK = "⚫️"
    GREEN = "🍀"


class Chat(Model):
    id: int = fields.IntField(pk=True, generated=False)
    messages_count: int = fields.IntField(default=0)

    last_person_of_day: datetime | None = fields.DatetimeField(null=True)
    last_casino: datetime | None = fields.DatetimeField(null=True)

    settings: fields.ReverseRelation["Setting"]
    users: fields.ReverseRelation["User"]


class User(Model):
    id: int = fields.IntField(pk=True, generated=False)
    is_admin = fields.BooleanField(default=False)
    is_owner = fields.BooleanField(default=False)
    custom_name: str | None = fields.CharField(max_length=255, null=True)
    messages_count: int = fields.IntField(default=0)
    sex_request: int | None = fields.IntField(null=True)

    # Money
    money: int = fields.IntField(default=0)
    last_bonus_use: datetime = fields.DatetimeField(null=True)

    # Dick
    dick_size: int = fields.IntField(default=0)
    last_dick_growth_use: datetime | None = fields.DatetimeField(null=True)

    # Casino
    casino_bet_amount: int = fields.IntField(null=True)
    casino_bet_color: CasinoChips | None = fields.CharEnumField(
        CasinoChips,
        max_length=5,
        null=True)

    # The Coin Game
    last_coin_game: datetime | None = fields.DatetimeField(null=True)

    chat: fields.ForeignKeyRelation[Chat] = fields.ForeignKeyField(
        'models.Chat', related_name='users')


class SettingType(IntEnum):
    bool = 0
    key = 1


class Setting(Model):
    id: int = fields.IntField(pk=True, generated=False)
    title: str = fields.CharField(max_length=255)
    value: int = fields.IntField()
    max_value: int = fields.IntField(default=1)
    type: SettingType = fields.IntEnumField(SettingType)

    chat: fields.ForeignKeyRelation[Chat] = fields.ForeignKeyField(
        'models.Chat', related_name='settings')


class Casino(Model):
    id: int = fields.IntField(pk=True)
    chat = fields.ForeignKeyField('models.Chat', related_name='casino')
    winner_feature: CasinoChips = fields.CharEnumField(
        CasinoChips,
        max_length=5)
