import re
from datetime import datetime
from random import choice, randint

import aiosqlite
from envparse import env
from pydantic import BaseModel
from pymorphy2 import MorphAnalyzer
from vkbottle.bot import Blueprint

# Иниты сюда
bp = Blueprint("Models")
morph = MorphAnalyzer()
env.read_envfile(".env")
DATABASE_PATH = "db.sqlite3"


class User():
    def __init__(self, chat_id: int, user_id: int) -> None:
        self.chat_id = chat_id
        self.user_id = user_id

    async def init(self):
        if self.user_id < 0:
            # Если передана группа,
            # то происходит экранизация класса Group
            self.group = Group(self.user_id)
        else:
            self.group = False

            # Регистрация юзера во избежания проблем
            if not await self.check():
                await self.register(0)

            sql = ("SELECT * FROM users WHERE chat_id = :chat_id "
                   "AND user_id = :user_id")
            sql_vars = {"chat_id": self.chat_id,
                        "user_id": self.user_id}

            async with aiosqlite.connect(DATABASE_PATH) as db:
                async with db.execute(sql, sql_vars) as cursor:
                    result = await cursor.fetchone()
            self.messages = result[2]
            self.custom_name = result[3]
            self.sex_request = result[4]
            self.money = result[5] or 0
            self.dick_size = result[6] or 0
            self.last_dick = result[7]
            self.is_admin = result[8] or False
            self.bonus_date = result[9]

    async def check(self, field: str = "user_id") -> list[int] | None:
        '''
        Проверяет заполнено ли передаваемое поле в БД
        '''
        if self.group is False:  # Проверка на группу
            sql = ("SELECT :field FROM users WHERE chat_id = :chat_id AND "
                   "user_id = :user_id")
            sql_vars = {"field": field,
                        "chat_id": self.chat_id,
                        "user_id": self.user_id}

            async with aiosqlite.connect(DATABASE_PATH) as db:
                async with db.execute(sql, sql_vars) as cursor:
                    return await cursor.fetchone()

    async def register(self, messages_count: int = 1) -> None:
        '''
        Регистрирует нового пользователя
        '''
        if self.group is False:  # Проверка на группу
            sql = ("INSERT INTO users (chat_id, user_id, messages, money) "
                   "VALUES (:chat_id, :user_id, :messages_count, 0)")
            sql_vars = {"chat_id": self.chat_id,
                        "user_id": self.user_id,
                        "messages_count": messages_count}

            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(sql, sql_vars)
                await db.commit()

    async def add_message(self) -> None:
        '''
        Добавляет сообщение в статистику
        '''
        if self.group is False:  # Проверка на группу
            sql = ("UPDATE users SET messages = :messages WHERE "
                   "chat_id = :chat_id AND user_id= :user_id")
            sql_vars = {"messages": self.messages + 1,
                        "chat_id": self.chat_id,
                        "user_id": self.user_id}

            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(sql, sql_vars)
                await db.commit()

    async def change_money(self, value):
        if self.group is False:  # Проверка на группу
            sql = ("UPDATE users SET money = :money WHERE "
                   "chat_id = :chat_id AND user_id= :user_id")
            sql_vars = {"money": self.money + value,
                        "chat_id": self.chat_id,
                        "user_id": self.user_id}

            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(sql, sql_vars)
                await db.commit()

    async def get_name(self, case: str = "nomn") -> str:
        '''
        Возращает имя юзера в необходимом падеже
        :param case: nomn | gent | datv | accs | ablt | loct | voct
        '''
        if self.group is False:  # Проверка на группу
            if self.custom_name is not None:
                raw_name = morph.parse(self.custom_name)[0]
                return raw_name.inflect(  # type: ignore
                    {case}).word.capitalize()
            else:
                vk_info = await bp.api.users.get(self.user_id)  # type: ignore
                try:
                    raw_name = morph.parse(vk_info[0].first_name)[0]
                    return raw_name.inflect(  # type: ignore
                        {case}).word.capitalize()
                except AttributeError:
                    return vk_info[0].first_name  # type: ignore
        else:
            return await self.group.get_name()

    async def test_custom_name(self, name: str):
        if len(name) > 35:
            return "words_count!"
        if re.search("^[а-я]+", name.lower()):
            try:
                raw_name = morph.parse(name)[0]
                cases = ["nomn", "gent", "datv",
                         "accs", "ablt", "loct", "voct"]
                for case in cases:
                    raw_name.inflect({case}).word.capitalize()
                return True
            except AttributeError:
                return "case!"
        else:
            return "words!"

    async def set_custom_name(self, name):
        if self.group is False:  # Проверка на группу
            sql = ("UPDATE users SET custom_name = :name WHERE "
                   "chat_id = :chat_id AND user_id = :user_id")
            sql_vars = {"name": name,
                        "chat_id": self.chat_id,
                        "user_id": self.user_id}

            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(sql, sql_vars)
                await db.commit()

    async def get_mention(self, case: str = "nomn") -> str:
        '''
        Возращает упоминания юзера в необходимом падеже
        :param case: nomn | gent | datv | accs | ablt | loct | voct
        '''
        if self.group is False:  # Проверка на группу
            return f"@id{self.user_id} ({await self.get_name(case)})"
        else:
            return await self.group.get_mention()

    async def get_sex(self):
        '''
        Возвращает пол пользователя.\n
        1 - девушка\n
        0 - парень
        '''
        if self.group is False:  # Проверка на группу
            return (await bp.api.users.get(self.user_id, "sex"))[0].sex.value

    async def update_last_bonus(self, date: datetime):
        sql = ("UPDATE users SET bonus_date = :date WHERE "
               "chat_id = :chat_id AND user_id = :user_id")
        sql_vars = {"date": date,
                    "chat_id": self.chat_id,
                    "user_id": self.user_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def change_dick(self, value):
        if self.group is False:  # Проверка на группу
            sql = ("UPDATE users SET dick_size = :size WHERE "
                   "chat_id = :chat_id AND user_id= :user_id")
            sql_vars = {"size": self.dick_size + value,
                        "chat_id": self.chat_id,
                        "user_id": self.user_id}

            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(sql, sql_vars)
                await db.commit()

    async def update_last_dick(self, date: int):
        sql = ("UPDATE users SET last_dick = :date WHERE "
               "chat_id = :chat_id AND user_id = :user_id")
        sql_vars = {"date": date,
                    "chat_id": self.chat_id,
                    "user_id": self.user_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def update_admin(self, value):
        sql = ("UPDATE users SET is_admin = :value WHERE "
               "chat_id = :chat_id AND user_id = :user_id")
        sql_vars = {"value": value,
                    "chat_id": self.chat_id,
                    "user_id": self.user_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()


class Group():
    def __init__(self, group_id: int) -> None:
        self.group_id = str(group_id)[1:]
        self.group_full_id = group_id

    async def get_name(self) -> str:
        '''
        Возращает имя группы из вк АПИ
        '''
        group_info = await bp.api.groups.get_by_id(self.group_id)
        return group_info[0].name

    async def get_mention(self) -> str:
        '''
        Возращает упоминание группы из вк АПИ
        '''
        return f"@club{self.group_id} ({await self.get_name()})"


class Chat():
    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id

    async def init(self):
        sql = "SELECT * FROM chats WHERE chat_id = :chat_id"
        sql_vars = {"chat_id": self.chat_id}

        if await self.check():
            async with aiosqlite.connect(DATABASE_PATH) as db:
                async with db.execute(sql, sql_vars) as cursor:
                    result = await cursor.fetchone()
            self.owner_id = result[1]
            self.messages = result[2]
            self.last_person_send = result[3]

    async def check(self) -> bool:
        '''
        Проверяет заполнено ли передаваемое поле в БД
        '''
        sql = "SELECT chat_id FROM chats WHERE chat_id = :chat_id"
        sql_vars = {"chat_id": self.chat_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchone()

    async def register(self, owner_id: int):
        '''
        Регистрирует новый чат
        '''
        sql = ("INSERT INTO chats (chat_id, owner_id, messages) VALUES "
               "(:chat_id, :owner_id, 1)")
        sql_vars = {"chat_id": self.chat_id,
                    "owner_id": owner_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def add_message(self):
        '''
        Добавляет сообщение в статистику
        '''
        sql = "UPDATE chats SET messages = :messages WHERE chat_id = :chat_id"
        sql_vars = {"messages": self.messages + 1,
                    "chat_id": self.chat_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def set_last_person_send(self, date) -> None:
        '''
        Обновляет дату последнего использования человека дня
        '''
        sql = ("UPDATE chats SET last_person_send = :date WHERE "
               "chat_id = :chat_id")
        sql_vars = {"date": date,
                    "chat_id": self.chat_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def get_dicks_top(self) -> list[int] | bool:
        sql = ("SELECT user_id FROM users WHERE chat_id = :chat_id "
               "AND dick_size <> 0 ORDER BY dick_size DESC")
        sql_vars = {"chat_id": self.chat_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchall() or False

    async def get_forbes_list(self) -> list[list[int]] | bool:
        sql = ("SELECT user_id FROM users WHERE chat_id = :chat_id "
               "AND money <> 0 ORDER BY money DESC")
        sql_vars = {"chat_id": self.chat_id}

        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchall() or False


class JSONSettings(BaseModel):
    setting: str
    alias: str
    value: str


class BaseSettings(BaseModel):
    settings: list[JSONSettings]


# default_settings = BaseSettings.parse_file("./default_settings.json")


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
        '''
        "from_user" предлагает секс переданному юзеру ("to_id")
        '''
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

    async def check(self) -> list:
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
