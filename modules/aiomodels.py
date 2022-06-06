import asyncio
import aiosqlite
from datetime import datetime
import re

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


class Chat:
    '''Описывает класс чата'''
    def __init__(self, id: int) -> None:
        self.chat_id = id

    async def _get_all_columns(self) -> tuple:
        '''Возвращает значение всех колонок по `self.chat_id`'''
        async with aiosqlite.connect(database) as db:
            sql = ("SELECT * FROM chats WHERE chat_id = :chat_id")
            sql_vars = {"chat_id": self.chat_id}
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
                if result is None:
                    raise RecordDoesNotExist
                return result

    async def _get(self) -> None:
        '''Заполняет `self` строками'''
        information = await self._get_all_columns()
        self.owner_id = information[1]
        self.messages = information[2]
        self.person_date = information[3]

    async def register(self, owner_id: int) -> None:
        '''Регистрирует чат в БД'''
        async with aiosqlite.connect(database) as db:
            sql = ("INSERT INTO chats (chat_id, owner_id, messages) VALUES "
                   "(:chat_id, :owner_id, 1)")
            sql_vars = {"chat_id": self.chat_id,
                        "owner_id": owner_id}
            await db.execute(sql, sql_vars)
            await db.commit()

    async def add_message(self, messages_count: int) -> None:
        '''Добавляет сообщения в статистику чата'''
        messages = self.messages + messages_count
        async with aiosqlite.connect(database) as db:
            sql = ("UPDATE chats SET messages = :messages WHERE "
                   "chat_id = :chat_id")
            sql_vars = {"chat_id": self.chat_id,
                        "messages": messages}
            await db.execute(sql, sql_vars)
            await db.commit()

    async def set_person_date(self, date: datetime) -> None:
        '''Обновляет дату последнего использования человека дня'''
        async with aiosqlite.connect(database) as db:
            sql = ("UPDATE chats SET person_date = :date WHERE "
                   "chat_id = :chat_id")
            sql_vars = {"chat_id": self.chat_id,
                        "date": date}
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
        async with aiosqlite.connect(database) as db:
            sql = ("SELECT * FROM accounts WHERE chat_id = :chat_id AND "
                   "id = :id")
            sql_vars = {"chat_id": self.chat.chat_id,
                        "id": self.id}
            async with db.execute(sql, sql_vars) as cursor:
                result = await cursor.fetchone()
                if result is None:
                    raise RecordDoesNotExist
                return result

    async def register(self) -> None:
        '''Регистрирует акаунт в БД'''
        async with aiosqlite.connect(database) as db:
            sql = ("INSERT INTO accounts (chat_id, id, messages) VALUES "
                   "(:chat_id, :id, 1)")
            sql_vars = {"chat_id": self.chat.chat_id,
                        "id": self.id}
            await db.execute(sql, sql_vars)
            await db.commit()

    async def _get(self) -> None:
        '''Заполняет `self` строками'''
        information = await self._get_all_columns()
        self.is_admin :int = information[2] or 0
        self.custom_name :str = information[3]
        self.messages :int = information[4]
        self.sex_request :int = information[5]
        self.money :int = information[6]
        self.bonus_date :datetime = information[7]
        self.dick_size :int = information[8]
        self.dick_date :datetime = information[8]

    async def _change_admin(self, value: int):
        async with aiosqlite.connect(database) as db:
            sql = ("UPDATE accounts SET is_admin = :value WHERE "
                   "chat_id = :chat_id AND id = :id")
            sql_vars = {"chat_id": self.chat.chat_id,
                        "id": self.id,
                        "value": value}
            await db.execute(sql, sql_vars)
            await db.commit()

    async def set_admin(self):
        '''Назначает акаунт админом'''
        await self._change_admin(1)

    async def unset_admin(self):
        '''Убирает админку у акаунта'''
        await self._change_admin(0)

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
        async with aiosqlite.connect(database) as db:
            sql = ("UPDATE accounts SET custom_name = :name WHERE "
                   "chat_id = :chat_id AND id = :id")
            sql_vars = {"chat_id": self.chat.chat_id,
                        "id": self.id,
                        "name": name}
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
            name = (await bp.api.groups.get_by_id(self.group_id))[0].name
        else:
            # Если кастомное имя не задано
            name = (await bp.api.users.get(self.user_id))[0].first_name

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
        async with aiosqlite.connect(database) as db:
            sql = ("UPDATE accounts SET money = :money WHERE "
                   "chat_id = :chat_id AND id = :id")
            sql_vars = {"chat_id": self.chat.chat_id,
                        "id": self.id,
                        "money": self.money + value}
            await db.execute(sql, sql_vars)
            await db.commit()

    async def update_bonus_date(self, date: datetime):
        '''Обновляет дату последнего получения бонуса'''
        async with aiosqlite.connect(database) as db:
            sql = ("UPDATE accounts SET bonus_date = :date WHERE "
                   "chat_id = :chat_id AND id = :id")
            sql_vars = {"chat_id": self.chat.chat_id,
                        "id": self.id,
                        "date": date}
            await db.execute(sql, sql_vars)
            await db.commit()

    async def change_dick(self, date: datetime, size: int):
        '''Обновляет дату и размер писюна'''
        async with aiosqlite.connect(database) as db:
            sql = ("UPDATE accounts SET dick_size = :size WHERE "
                   "chat_id = :chat_id AND id = :id")
            sql_vars = {"chat_id": self.chat.chat_id,
                        "id": self.id,
                        "size": self.dick_size + size}
            await db.execute(sql, sql_vars)

            sql = ("UPDATE accounts SET dick_date = :date WHERE "
                   "chat_id = :chat_id AND id = :id")
            sql_vars = {"chat_id": self.chat.chat_id,
                        "id": self.id,
                        "date": date}
            await db.execute(sql, sql_vars)
            await db.commit()


async def chat_test():
    chat = Chat(100)
    try:
        await chat._get()
        await chat.add_message(1)
        await chat.set_person_date(datetime.now())
        print(chat.messages)
    except RecordDoesNotExist:
        print("Чат не зареган! Идёт регистрация")
        await chat.register(1)


async def user_test():
    account = Account(100, 356467032)
    try:
        await account.test_custom_name("Дима шип")
        await account._get()
        print(await account.get_mention("datv"))
        if not account.is_admin:
            await account.set_admin()
            print("акаунт стал админом!")
        else:
            await account.unset_admin()
            print("акаунт теперь не админ!")
    except RecordDoesNotExist:
        await account.register()
