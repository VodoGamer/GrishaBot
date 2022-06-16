import re
from datetime import datetime
from random import choice, randint
from typing import Any

import aiosqlite
from envparse import env
from pydantic import BaseModel
from pymorphy2 import MorphAnalyzer
from vkbottle.bot import Blueprint

# Иниты сюда
bp = Blueprint("Models")
morph = MorphAnalyzer()
env.read_envfile(".env")
DATABASE_PATH = (env.str("DB_PATH"))


# execptions
class ObjectDoesNotExist(Exception):
    def __init__(self, text: str):
        self.txt = text


# custom names execptions
class NameLongerThan35Characters(Exception):
    def __init__(self, text: str):
        self.txt = text


class RussianWordsOnly(Exception):
    def __init__(self, text: str):
        self.txt = text


class TheNameDoesNotIncline(Exception):
    def __init__(self, text: str):
        self.txt = text


class Chat():
    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id
        self._info = False

    async def _get_all_columns(self):
        sql = ("SELECT * FROM chats WHERE chat_id = :chat_id")
        sql_vars = {"chat_id": self.chat_id}
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchone()

    async def _init(self):
        if not self._info:
            all_columns = await self._get_all_columns()
            if not bool(all_columns):
                raise ObjectDoesNotExist("Chat does not exist!")
            result = all_columns  # type: ignore

            self.owner_id: int = result[1]
            self.messages: int = result[2]
            self.last_person_send: datetime = result[3]
            self._info = True

    async def _change_value(self, column: str, new_value: Any):
        '''Обновляет строку'''
        sql = (f"UPDATE chats SET {column} = :new_value WHERE "
               "chat_id = :chat_id")
        sql_vars = {"new_value": new_value,
                    "chat_id": self.chat_id}
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def register(self, owner_id: int):
        '''Регистрирует новый чат'''
        sql = ("INSERT INTO chats (chat_id, owner_id, messages) VALUES "
               "(:chat_id, :owner_id, 1)")
        sql_vars = {"chat_id": self.chat_id,
                    "owner_id": owner_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def add_message(self):
        '''Добавляет сообщение в статистику'''
        await self._init()
        await self._change_value("messages", self.messages + 1)

    async def set_last_person_send(self, date) -> None:
        '''Обновляет дату последнего использования человека дня'''
        await self._change_value("last_person_send", date)

    async def _get_top(self, column):
        sql = ("SELECT user_id FROM users WHERE chat_id = :chat_id "
               f"AND {column} <> 0 ORDER BY {column} DESC")
        sql_vars = {"chat_id": self.chat_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchall()

    async def get_dicks_top(self):
        return await self._get_top("dick_size")

    async def get_forbes_list(self):
        return await self._get_top("money")


class Account():
    def __init__(self, chat_id: int, user_id: int) -> None:
        self.chat_id = chat_id
        self.user_id = user_id
        self._info = False

    async def _get_all_columns(self):
        sql = ("SELECT * FROM users WHERE chat_id = :chat_id "
               "AND user_id = :user_id")
        sql_vars = {"chat_id": self.chat_id,
                    "user_id": self.user_id}
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchone()

    async def _init(self):
        if not self._info:
            all_columns = await self._get_all_columns()
            if not bool(all_columns):
                raise ObjectDoesNotExist("User does not exist!")
            result = all_columns  # type: ignore

            self.messages: int = result[2]
            self.custom_name: str = result[3]
            self.sex_request: int = result[4]
            self.money: int = result[5] or 0
            self.dick_size: int = result[6] or 0
            self.last_dick: int = result[7]
            self.is_admin: int = result[8] or False
            self.bonus_date: datetime = result[9]

            self.chat = Chat(self.chat_id)
            self._info = True

    async def _change_value(self, column: str, new_value: Any):
        '''Обновляет строку'''
        sql = (f"UPDATE users SET {column} = :new_value WHERE "
               "chat_id = :chat_id AND user_id= :user_id")
        sql_vars = {"new_value": new_value,
                    "chat_id": self.chat_id,
                    "user_id": self.user_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def register(self, messages_count: int=1) -> None:
        '''Регистрирует нового пользователя'''
        if not await self._get_all_columns():
            sql = ("INSERT INTO users (chat_id, user_id, messages) "
                    "VALUES (:chat_id, :user_id, :messages_count)")
            sql_vars = {"chat_id": self.chat_id,
                        "user_id": self.user_id,
                        "messages_count": messages_count}

            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(sql, sql_vars)
                await db.commit()

    async def add_message(self, messages_count: int=1) -> None:
        '''Добавляет сообщение в статистику'''
        await self._init()

        await self._change_value("messages", self.messages + messages_count)

    async def change_money(self, value: int):
        '''Меняет кол-во денег акаунта'''
        await self._init()

        await self._change_value("money", self.money + value)

    async def get_name(self, case: str="nomn") -> str:
        '''
        Возращает имя юзера в необходимом падеже
        :param case: nomn | gent | datv | accs | ablt | loct | voct
        '''
        await self._init()

        if self.custom_name:
            names = self.custom_name
        elif self.user_id < 0:
            names = (await bp.api.groups.get_by_id(
                self.group_id))[0].name  # type: ignore
        else:
            names = (await bp.api.users.get(
                self.user_id))[0].first_name  # type: ignore
        try:
            multi_names = []

            for name in names.split(' '):  # type: ignore
                raw_name = morph.parse(name)[0]
                multi_names.append(
                    raw_name.inflect({case}).word)  # type: ignore
            return " ".join(multi_names).capitalize()
        except AttributeError:
            return name  # type: ignore

    async def test_custom_name(self, names: str) -> bool:
        if len(names) > 35:
            raise NameLongerThan35Characters("custom name doesn't fit")
        if not re.search("^[а-я]+", names.lower()):
            raise RussianWordsOnly("custom name doesn't fit")
        try:
            cases = ["nomn", "gent", "datv",
                     "accs", "ablt", "loct",
                     "voct"]
            for case in cases:
                for name in names.split(' '):  # type: ignore
                    raw_name = morph.parse(name)[0]
                    raw_name.inflect({case}).word  # type: ignore
            return True
        except AttributeError:
            raise TheNameDoesNotIncline("custom name doesn't fit")

    async def set_custom_name(self, name: str):
        await self._change_value("custom_name", name)

    async def get_mention(self, case: str = "nomn") -> str:
        '''
        Возращает упоминание юзера в необходимом падеже
        :param case: nomn | gent | datv | accs | ablt | loct | voct
        '''
        if self.user_id > 0:  # Проверка на пользователя
            return f"@id{self.user_id} ({await self.get_name(case)})"
        else:
            return f"@club{self.user_id} ({await self.get_name(case)})"

    async def get_sex(self):
        '''
        Возвращает пол пользователя.\n
        1 - девушка\n
        0 - парень
        '''
        if self.user_id < 0:
            return 0
        return (await bp.api.users.get(
            self.user_id, "sex"))[0].sex.value  # type: ignore

    async def update_last_bonus(self, date: datetime):
        await self._change_value("bonus_date", date)

    async def change_dick(self, value: int):
        await self._init()
        await self._change_value("dick_size", self.dick_size + value)

    async def update_last_dick(self, date: datetime):
        await self._change_value("last_dick", date)

    async def update_admin(self, value: int):
        await self._change_value("is_admin", value)


class JSONSettings(BaseModel):
    setting: str
    alias: str
    value: str


class BaseSettings(BaseModel):
    settings: list[JSONSettings]


default_settings = BaseSettings.parse_file("./default_settings.json")


class Settings():
    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id

    async def update(self):
        for i in default_settings.settings:
            if not await self.get_alias(i.alias):
                await self.add(i.setting, i.alias, i.value)

    async def check(self):
        '''
        Проверяет есть ли чат в талице settings
        '''
        sql = "SELECT chat_id FROM settings WHERE chat_id = :chat_id"
        sql_vars = {"chat_id": self.chat_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchone()

    async def add(self, setting, alias, value):
        '''Добавляет новую настройку'''
        setting = setting.lower()
        alias = alias.lower()
        sql = ("INSERT INTO settings (chat_id, setting, alias, value) VALUES "
               "(:chat_id, :setting, :alias, :value)")
        sql_vars = {"chat_id": self.chat_id,
                    "setting": setting,
                    "alias": alias,
                    "value": value}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def get_value(self, alias):
        sql = ("SELECT value FROM settings WHERE "
               "chat_id = :chat_id AND alias = :alias")
        sql_vars = {"chat_id": self.chat_id,
                    "alias": alias}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchone()

    async def get_alias(self, alias):
        sql = ("SELECT alias FROM settings WHERE "
               "chat_id = :chat_id AND alias = :alias")
        sql_vars = {"chat_id": self.chat_id,
                    "alias": alias}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchone()

    async def get_all(self):
        '''
        Вовращает все настройки чата
        '''
        sql = "SELECT * FROM settings WHERE chat_id = :chat_id"
        sql_vars = {"chat_id": self.chat_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchall()

    async def change_value(self, alias: str, value=None):
        '''
        Меняет значение value передаваемой настройки на противоположное
        '''
        alias = alias.lower()
        res = (await self.get_value(alias))[0]
        if res == "True":
            value = "False"
            value_return = "❌"
        elif res == "False":
            value = "True"
            value_return = "✅"
        else:
            if value == '':
                raise ValueError
            value_return = value
        sql = ("UPDATE settings SET value = :value WHERE "
               "chat_id = :chat_id AND alias = :alias")
        sql_vars = {"value": value,
                    "chat_id": self.chat_id,
                    "alias": alias}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()
        return value_return

    async def get_alias_by_setting(self, setting):
        setting = setting.lower()
        sql = ("SELECT alias FROM settings WHERE chat_id = :chat_id "
               "AND setting = :setting")
        sql_vars = {"chat_id": self.chat_id,
                    "setting": setting}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchone()


class Sex():
    def __init__(self, chat_id: int, from_user: int) -> None:
        self.chat_id = chat_id
        self.from_user = from_user

    async def start(self, to_id) -> None:
        '''"from_user" предлагает секс переданному юзеру ("to_id")'''
        sql = ("UPDATE users SET sex_request = :request WHERE "
               "chat_id = :chat_id AND user_id = :user_id")
        sql_vars = {"chat_id": self.chat_id,
                    "request": self.from_user,
                    "user_id": to_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def get_request(self) -> None | int:
        '''
        есть ли запрос на секс у "from_user" от другого юзера
        возвращает id другого юзера
        '''
        sql = ("SELECT sex_request FROM users WHERE chat_id = :chat_id "
               "AND user_id = :user_id")
        sql_vars = {"chat_id": self.chat_id,
                    "user_id": self.from_user}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    async def get_send(self) -> None | int:
        '''
        отправлял ли "from_user" запрос на секс другому
        возращает id другого юзера
        '''

        sql = ("SELECT user_id FROM users WHERE chat_id = :chat_id "
               "AND sex_request = :request")
        sql_vars = {"chat_id": self.chat_id,
                    "request": self.from_user}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    async def end_sex(self, to_id):
        '''
        убирает заявку на секс отправленную от "from_user"
        '''
        sql = ("UPDATE users SET sex_request = Null WHERE chat_id = :chat_id "
               "AND user_id = :user_id")
        sql_vars = {"chat_id": self.chat_id,
                    "user_id": to_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def discard_sex(self):
        '''
        отклонение "from_user" от предложения секса другого юзера
        '''
        sql = ("UPDATE users SET sex_request = Null WHERE chat_id = :chat_id "
               "AND user_id = :user_id")
        sql_vars = {"chat_id": self.chat_id,
                    "user_id": self.from_user}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()


class CasinoUser():
    def __init__(self, chat_id: int, user_id: int) -> None:
        self.chat_id = chat_id
        self.user_id = user_id

    async def init(self):
        user_info = await self.check()
        if user_info is not None:
            self.bet = user_info[2]
            self.feature = user_info[3]

    async def check(self):
        '''
        Проверяет учавствует ли юзер в крутке
        '''
        sql = ("SELECT * FROM casino WHERE chat_id = :chat_id AND "
               "user_id = :user_id")
        sql_vars = {"chat_id": self.chat_id,
                    "user_id": self.user_id}
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchone()

    async def register_bet(self, bet: int, feature: str):
        '''
        Регистрирует пользователя в крутку
        '''
        sql = ("INSERT INTO casino (chat_id, user_id, bet, feature) "
               "VALUES (:chat_id, :user_id, :bet, :feature)")
        sql_vars = {"chat_id": self.chat_id,
                    "user_id": self.user_id,
                    "bet": bet,
                    "feature": feature}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()


class Casino():
    def __init__(self, chat_id) -> None:
        self.chat_id = chat_id

    async def get_users(self) -> list[tuple[int, int, int, str]]:
        sql = "SELECT * FROM casino WHERE chat_id = :chat_id"
        sql_vars = {"chat_id": self.chat_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchall()

    async def get_winner_users(self, feature: str) -> list[int]:
        sql = ("SELECT user_id FROM casino WHERE chat_id = :chat_id "
               "AND feature = :feature")
        sql_vars = {"chat_id": self.chat_id,
                    "feature": feature}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                users = await cursor.fetchall()
        result = []
        for user in users:
            result.append(user[0])
        return result

    async def get_winner_feature(self) -> str:
        if randint(1, 10) == 1:
            return "🍀"
        return choice(["🔴", "⚫️"])

    async def delete_all(self):
        sql = "DELETE FROM casino WHERE chat_id = :chat_id"
        sql_vars = {"chat_id": self.chat_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def add_to_history(self, feature: str):
        now = datetime.now()
        sql = ("INSERT INTO casino_history "
               "(chat_id, date, time, win_feature) VALUES "
               "(:chat_id, :date, :time, :feature)")
        sql_vars = {"chat_id": self.chat_id,
                    "date": now.date(),
                    "time": str(now.time()),
                    "feature": feature}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def get_history(self) -> list[str] | None:
        now = datetime.now()
        sql = ("SELECT win_feature FROM casino_history WHERE "
               "chat_id = :chat_id AND date = :date ORDER BY "
               "time LIMIT 20")
        sql_vars = {"chat_id": self.chat_id,
                    "date": now.date()}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                features = await cursor.fetchall()
        if features == []:
            return None
        else:
            feature_list = []
            for feature in features:
                feature_list.append(feature[0])
            return feature_list

    async def get_last_go(self) -> datetime:
        now = datetime.now()
        sql = ("SELECT time FROM casino_history WHERE "
               "chat_id = :chat_id AND date = :date ORDER BY time DESC")
        sql_vars = {"chat_id": self.chat_id,
                    "date": now.date()}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
        if result is None:
            return True
        else:
            return result[0]
