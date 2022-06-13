import asyncio
import re
from datetime import datetime
from random import choice, randint

import aiosqlite
from pydantic import BaseModel
from pymorphy2 import MorphAnalyzer
from vkbottle.bot import Blueprint

# Иниты сюда
bp = Blueprint("AioModels")
morph = MorphAnalyzer()
database = "db.db"


# Exceptions
class RecordDoesNotExist(Exception):
    ...


class LenCustomNameError(Exception):
    ...


class NoEnlgishCustomName(Exception):
    ...


class IncorrectCaseCustomName(Exception):
    ...


class BoolSettingDoesNotRandomInt(Exception):
    ...


class FromUserDoesntHaveSexRequest(Exception):
    ...


class FromUserDontSendSexRequest(Exception):
    ...


class Chat:
    '''Описывает класс чата'''

    def __init__(self, id: int) -> None:
        self.chat_id = id

    async def _get_all_columns(self) -> tuple:
        '''Возвращает значение всех колонок по `self.chat_id`'''
        sql = ("SELECT * FROM chats WHERE chat_id = :chat_id")
        sql_vars = {"chat_id": self.chat_id}
        async with aiosqlite.connect(database) as db:
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
        if result is None:
            raise RecordDoesNotExist
        return result

    async def get(self) -> None:
        '''Заполняет `self` строками'''
        information = await self._get_all_columns()
        self.owner_id: int = information[1]
        self.messages: int = information[2]
        self.person_date: datetime = information[3]

    async def register(self, owner_id: int) -> None:
        '''Регистрирует чат в БД'''
        sql = ("INSERT INTO chats (chat_id, owner_id, messages) VALUES "
               "(:chat_id, :owner_id, 1)")
        sql_vars = {"chat_id": self.chat_id,
                    "owner_id": owner_id}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def add_message(self, messages_count: int) -> None:
        '''Добавляет сообщения в статистику чата'''
        messages = self.messages + messages_count
        sql = ("UPDATE chats SET messages = :messages WHERE "
               "chat_id = :chat_id")
        sql_vars = {"chat_id": self.chat_id,
                    "messages": messages}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def set_person_date(self, date: datetime) -> None:
        '''Обновляет дату последнего использования человека дня'''
        sql = ("UPDATE chats SET person_date = :date WHERE "
               "chat_id = :chat_id")
        sql_vars = {"chat_id": self.chat_id,
                    "date": date}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()


class Account:
    '''Описывает класс акаунта(ботов и юзеров)'''

    def __init__(self, chat_id: int, id: int) -> None:
        self.chat = Chat(chat_id)
        self.id = id

    async def _get_all_columns(self) -> tuple:
        '''Возвращает значение всех колонок по `self.id` и
        `self.chat.chat_id`'''
        sql = ("SELECT * FROM accounts WHERE chat_id = :chat_id AND "
               "id = :id")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.id}
        async with aiosqlite.connect(database) as db:
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
        if result is None:
            raise RecordDoesNotExist
        return result

    async def register(self) -> None:
        '''Регистрирует акаунт в БД'''
        sql = ("INSERT INTO accounts (chat_id, id, messages) VALUES "
               "(:chat_id, :id, 1)")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.id}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def get(self) -> None:
        '''Заполняет `self` строками'''
        information = await self._get_all_columns()
        self.is_admin: int = information[2] or 0
        self.custom_name: str = information[3]
        self.messages: int = information[4]
        self.sex_request: int = information[5]
        self.money: int = information[6]
        self.bonus_date: datetime = information[7]
        self.dick_size: int = information[8]
        self.dick_date: datetime = information[8]

    async def change_admin(self, value: int):
        sql = ("UPDATE accounts SET is_admin = :value WHERE "
               "chat_id = :chat_id AND id = :id")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.id,
                    "value": value}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def set_admin(self):
        '''Назначает акаунт админом'''
        await self.change_admin(1)

    async def unset_admin(self):
        '''Убирает админку у акаунта'''
        await self.change_admin(0)

    async def test_custom_name(self, name: str) -> None:
        '''Проверяет кастомное имя'''
        if len(name) > 35:
            # проверка на длину имени
            raise LenCustomNameError
        if not re.search("^[а-я]+", name.lower()):
            # проверка на наличие других символов, кроме русских
            raise NoEnlgishCustomName

        try:
            # проверка на скольняемость слова
            cases = ["nomn", "gent", "datv",
                     "accs", "ablt", "loct", "voct"]
            for case in cases:
                for i in name.split():
                    morph.parse(i)[0].inflect({case}).word
        except AttributeError as e:
            raise IncorrectCaseCustomName

    async def set_custom_name(self, name: str) -> None:
        '''Устанавливает кастомное имя'''
        sql = ("UPDATE accounts SET custom_name = :name WHERE "
               "chat_id = :chat_id AND id = :id")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.id,
                    "name": name}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def get_name(self, case):
        '''
        Возращает имя акаунта в необходимом падеже
        :param case: nomn | gent | datv | accs | ablt | loct | voct
        '''
        if self.custom_name:
            name = self.custom_name
        elif self.id < 0:
            # Если кастомное имя не задано и это группа
            name = (await bp.api.groups.get_by_id(self.id))[0].name
        else:
            # Если кастомное имя не задано
            name = (await bp.api.users.get(self.id))[0].first_name

        try:
            multi_name = []
            for i in name.split():
                multi_name.append(morph.parse(i)[0].inflect({case}).word)
            return ' '.join(multi_name).capitalize()
        except AttributeError:
            return name

    async def get_mention(self, case):
        '''
        Возращает упоминания акаунта в необходимом падеже
        :param case: nomn | gent | datv | accs | ablt | loct | voct
        '''
        if self.id < 0:
            return f"@club{self.id} ({await self.get_name(case)})"
        return f"@id{self.id} ({await self.get_name(case)})"

    async def add_money(self, value: int):
        '''Добавляет деньги акаунту'''
        sql = ("UPDATE accounts SET money = :money WHERE "
               "chat_id = :chat_id AND id = :id")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.id,
                    "money": self.money + value}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def update_bonus_date(self, date: datetime):
        '''Обновляет дату последнего получения бонуса'''
        sql = ("UPDATE accounts SET bonus_date = :date WHERE "
               "chat_id = :chat_id AND id = :id")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.id,
                    "date": date}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def change_dick(self, date: datetime, size: int):
        '''Обновляет дату и размер писюна'''
        sql = ("UPDATE accounts SET dick_size = :size WHERE "
               "chat_id = :chat_id AND id = :id")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.id,
                    "size": self.dick_size + size}

        sql2 = ("UPDATE accounts SET dick_date = :date WHERE "
                "chat_id = :chat_id AND id = :id")
        sql2_vars = {"chat_id": self.chat.chat_id,
                     "id": self.id,
                     "date": date}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.execute(sql2, sql2_vars)
            await db.commit()


# Settings JSON classes
class JSONSettings(BaseModel):
    id: int
    alias: str
    value: int
    disabled: bool
    boolable: int


class BaseSettings(BaseModel):
    settings: list[JSONSettings]


default_settings = BaseSettings.parse_file("./default_settings.json")


class Setting:
    def __init__(self, chat_id: int, setting_id: int) -> None:
        self.chat = Chat(chat_id)
        self.setting_id = setting_id

    async def _get_all_columns(self) -> tuple:
        '''Возвращает значение всех колонок по и `self.chat.chat_id`'''
        sql = ("SELECT * FROM settings WHERE chat_id = :chat_id AND "
               "setting_id = :id")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.setting_id}
        async with aiosqlite.connect(database) as db:
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
        if result is None:
            raise RecordDoesNotExist
        return result

    async def get(self):
        '''Заполняет `self` строками'''
        information = await self._get_all_columns()
        self.value: int = information[3]
        self.alias: str = default_settings.settings[self.setting_id - 1].alias
        self.boolable: int = information[4]

    async def add(self, value: int, title: str, boolable: int):
        '''Добавляет новую настройку к чату'''
        sql = ("INSERT INTO settings (chat_id, setting_id, value, "
               "title, boolable) "
               "VALUES (:chat_id, :id, :value, :title, :boolable)")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.setting_id,
                    "value": value,
                    "title": title,
                    "boolable": boolable}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def delete(self):
        '''Удаляет настройку у чата'''
        sql = ("DELETE FROM settings WHERE chat_id = :chat_id "
               "AND setting_id = :id")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.setting_id}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def change_title(self, new_title: str):
        '''Изменяет название настройки в БД'''
        sql = ("UPDATE settings SET title = :title WHERE "
               "chat_id = :chat_id AND setting_id = :id")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.setting_id,
                    "title": new_title}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def change_value(self, value: int):
        '''Изменяет значение настройки в БД'''
        if self.boolable and value >= 2:
            raise BoolSettingDoesNotRandomInt
        sql = ("UPDATE settings SET value = :value WHERE "
               "chat_id = :chat_id AND setting_id = :id")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "id": self.setting_id,
                    "value": value}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()


class Settings:
    def __init__(self, chat_id: int) -> None:
        self.chat = Chat(chat_id)

    async def register_all(self):
        '''Регистрирует все настройки для нового чата'''
        for setting in default_settings.settings:
            setting_class = Setting(self.chat.chat_id, setting.id)
            await setting_class.add(setting.value,
                                    setting.alias,
                                    setting.boolable)

    async def get_all(self) -> list[int, str, int]:
        '''Получает все настройки чата'''
        sql = ("SELECT setting_id, title, value FROM settings "
               "WHERE chat_id = :chat_id")
        sql_vars = {"chat_id": self.chat.chat_id}
        async with aiosqlite.connect(database) as db:
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchall()
        if result is None:
            raise RecordDoesNotExist
        return result


class Sex():
    def __init__(self, chat_id: int, from_user: int) -> None:
        self.chat_id = chat_id
        self.from_user = from_user

    async def start(self, to_id) -> None:
        '''
        "from_user" предлагает секс переданному юзеру ("to_id")
        '''
        sql = ("UPDATE accounts SET sex_request = :request WHERE "
               "chat_id = :chat_id AND user_id = :user_id")
        sql_vars = {"chat_id": self.chat_id,
                    "request": self.from_user,
                    "user_id": to_id}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def get_request(self) -> int:
        '''
        есть ли запрос на секс у "from_user" от другого юзера
        возвращает id другого юзера
        '''
        sql = ("SELECT sex_request FROM accounts WHERE chat_id = :chat_id "
               "AND user_id = :user_id")
        sql_vars = {"chat_id": self.chat_id,
                    "user_id": self.from_user}

        async with aiosqlite.connect(database) as db:
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
        if result is None:
            raise FromUserDoesntHaveSexRequest
        else:
            return result[0]

    async def get_send(self) -> int:
        '''
        отправлял ли "from_user" запрос на секс другому
        возращает id другого юзера
        '''

        sql = ("SELECT user_id FROM accounts WHERE chat_id = :chat_id "
               "AND sex_request = :request")
        sql_vars = {"chat_id": self.chat_id,
                    "request": self.from_user}

        async with aiosqlite.connect(database) as db:
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
        if result is None:
            raise FromUserDontSendSexRequest
        else:
            return result[0]

    async def end_sex(self, to_id):
        '''
        убирает заявку на секс отправленную от "from_user"
        '''
        sql = ("UPDATE accounts SET sex_request = Null WHERE "
               "chat_id = :chat_id AND user_id = :user_id")
        sql_vars = {"chat_id": self.chat_id,
                    "user_id": to_id}

        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def discard_sex(self):
        '''
        отклонение "from_user" от предложения секса другого юзера
        '''
        sql = ("UPDATE accounts SET sex_request = Null WHERE "
               "chat_id = :chat_id AND user_id = :user_id")
        sql_vars = {"chat_id": self.chat_id,
                    "user_id": self.from_user}

        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()


class CasinoUser():
    def __init__(self, chat_id: int, user_id: int) -> None:
        self.chat = Chat(chat_id)
        self.user_id = user_id

    async def _get_all_columns(self):
        '''Возвращает значение всех колонок по `self.chat_id`'''
        sql = ("SELECT * FROM casino WHERE chat_id = :chat_id AND "
               "user_id = :user_id")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "user_id": self.user_id}
        async with aiosqlite.connect(database) as db:
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
        if result is None:
            raise RecordDoesNotExist
        return result

    async def get(self):
        information = self._get_all_columns()
        self.bet = information[2]
        self.feature = information[3]

    async def register_bet(self, bet: int, feature: str):
        '''
        Регистрирует пользователя в крутку
        '''
        sql = ("INSERT INTO casino (chat_id, user_id, bet, feature) "
               "VALUES (:chat_id, :user_id, :bet, :feature)")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "user_id": self.user_id,
                    "bet": bet,
                    "feature": feature}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()


class Casino():
    def __init__(self, chat_id) -> None:
        self.chat = Chat(chat_id)

    async def get_users(self):
        sql = "SELECT * FROM casino WHERE chat_id = :chat_id"
        sql_vars = {"chat_id": self.chat.chat_id}
        async with aiosqlite.connect(database) as db:
            async with db.execute(sql, sql_vars) as cursor:
                return await cursor.fetchone()

    async def get_winner_users(self, feature: str) -> list[int]:
        sql = ("SELECT user_id FROM casino WHERE chat_id = :chat_id "
               "AND feature = :feature")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "feature": feature}
        async with aiosqlite.connect(database) as db:
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
        sql_vars = {"chat_id": self.chat.chat_id}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def add_to_history(self, feature: str):
        now = datetime.now()
        sql = ("INSERT INTO casino_history "
               "(chat_id, date, time, win_feature) VALUES "
               "(:chat_id, :date, :time, :feature)")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "date": now.date(),
                    "time": str(now.time()),
                    "feature": feature}
        async with aiosqlite.connect(database) as db:
            await db.execute(sql, sql_vars)
            await db.commit()

    async def get_history(self) -> list[str] | None:
        now = datetime.now()
        sql = ("SELECT win_feature FROM casino_history WHERE "
               "chat_id = :chat_id AND date = :date ORDER BY "
               "time LIMIT 20")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "date": now.date()}
        async with aiosqlite.connect(database) as db:
            async with db.execute(sql, sql_vars) as cursor:
                features = await cursor.fetchall()
        if features == []:
            return None
        else:
            feature_list = []
            for feature in features:
                feature_list.append(feature[0])
            return feature_list

    async def get_last_go(self):
        now = datetime.now()
        sql = ("SELECT time FROM casino_history WHERE "
               "chat_id = :chat_id AND date = :date ORDER BY time DESC")
        sql_vars = {"chat_id": self.chat.chat_id,
                    "date": now.date()}
        async with aiosqlite.connect(database) as db:
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
        if result is None:
            return True
        else:
            return result[0]


# Settings init
async def settings_upgrade():
    '''Функция, запускающаяся при запуске бота. Проверяет JSON на наличие
    новых настроек или задизабленных настроек. Также проверяет настройки на
    смену тайтла (алиса). Выполняется один раз, при каждом запуске бота.'''
    sql = ("SELECT chat_id FROM chats")
    async with aiosqlite.connect(database) as db:
        async with db.execute(sql) as cursor:
            chats = await cursor.fetchall()

    for chat in chats:
        for setting in default_settings.settings:
            sql = (f"SELECT * FROM settings WHERE chat_id = {chat[0]} "
                   f"AND setting_id = {setting.id}")
            async with aiosqlite.connect(database) as db:
                async with db.execute(sql) as cursor:
                    result = await cursor.fetchone()
            setting_class = Setting(chat[0], setting.id)
            if setting.disabled and result:
                await setting_class.delete()
            else:
                if result is None:
                    await setting_class.add(setting.value, setting.alias,
                                            setting.boolable)
                    continue
                if result[2] != setting.alias:
                    await setting_class.change_title(setting.alias)

asyncio.run(settings_upgrade())
