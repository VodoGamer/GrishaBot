'''all bot's models'''
from datetime import datetime
from enum import Enum

from tortoise import fields
from tortoise.models import Model


class CasinoChips(Enum):
    RED = "🔴"
    BLACK = "⚫️"
    GREEN = "🍀"


class Chat(Model):
    id: int = fields.IntField(pk=True, generated=False)
    owner_id: int = fields.IntField(null=True)
    messages_count: int = fields.IntField(default=1)
    last_person_of_day_use: datetime = fields.DatetimeField(null=True)
    last_casino_use: datetime = fields.DatetimeField(null=True)
    last_shop_message_id: int | None = fields.IntField(null=True)


class User(Model):
    id: int = fields.IntField(pk=True, generated=False)
    chat = fields.ForeignKeyField('models.Chat', related_name='users')
    is_admin: bool = fields.BooleanField(default=False)  # type: ignore
    custom_name: str = fields.CharField(max_length=255, null=True)
    messages_count: int = fields.IntField(default=1)
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


class Setting(Model):
    id: int = fields.IntField(pk=True, generated=False)
    chat = fields.ForeignKeyField('models.Chat', related_name='settings')
    title: str = fields.CharField(max_length=255)
    value: int = fields.IntField()
    max_value: int = fields.IntField(default=1)


class Casino(Model):
    id: int = fields.IntField(pk=True)
    chat = fields.ForeignKeyField('models.Chat', related_name='casino')
    winner_feature: CasinoChips = fields.CharEnumField(
        CasinoChips,
        max_length=5)
