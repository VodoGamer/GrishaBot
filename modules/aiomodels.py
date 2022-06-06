import asyncio
import aiosqlite
from datetime import datetime
from random import choice, randint
import re

from pydantic import BaseModel
from pymorphy2 import MorphAnalyzer
from vkbottle.bot import Blueprint


# Иниты сюда
bp = Blueprint("AioModels")
morph = MorphAnalyzer()


# Exceptions
class RecordDoesNotExist(Exception):
    ...


class Chat:
    '''Описывает класс чата'''
    def __init__(self, id: int) -> None:
        self.chat_id = id

    async def _get_all_columns(self) -> tuple:
        '''Возвращает значение всех колонок по `self.chat_id`'''
        async with aiosqlite.connect("db.db") as db:
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
        async with aiosqlite.connect("db.db") as db:
            sql = ("INSERT INTO chats (chat_id, owner_id, messages) VALUES "
                   "(:chat_id, :owner_id, 1)")
            sql_vars = {"chat_id": self.chat_id,
                        "owner_id": owner_id}
            await db.execute(sql, sql_vars)
            await db.commit()

    async def add_message(self, messages_count: int) -> None:
        '''Добавляет сообщения в статистику чата'''
        messages = self.messages + messages_count
        async with aiosqlite.connect("db.db") as db:
            sql = ("UPDATE chats SET messages = :messages WHERE "
                   "chat_id = :chat_id")
            sql_vars = {"chat_id": self.chat_id,
                        "messages": messages}
            await db.execute(sql, sql_vars)
            await db.commit()

    async def set_person_date(self, date: datetime) -> None:
        '''Обновляет дату последнего использования человека дня'''
        async with aiosqlite.connect("db.db") as db:
            sql = ("UPDATE chats SET person_date = :date WHERE "
                   "chat_id = :chat_id")
            sql_vars = {"chat_id": self.chat_id,
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
