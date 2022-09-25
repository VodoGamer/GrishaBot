from enum import IntEnum
from typing import NamedTuple


class SettingType(IntEnum):
    bool = 0
    int = 1


class Setting(NamedTuple):
    id: int
    title: str
    type: SettingType
    default_value: int
    max_value: int | None = None


messages_pin = Setting(
    id=1,
    title="Закреп сообщений, отправляемых ботом",
    type=SettingType.bool,
    default_value=0,)

casino = Setting(
    id=2,
    title="Казино",
    type=SettingType.bool,
    default_value=0,)

casino_cooldown = Setting(
    id=3,
    title=" Кд на команду: \"го\"",
    type=SettingType.int,
    default_value=10,
    max_value=300)

stickers = Setting(
    id=4,
    title="Использование стикеров ботом",
    type=SettingType.bool,
    default_value=0,)


settings = (messages_pin, casino, casino_cooldown, stickers)
