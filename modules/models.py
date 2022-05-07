import sqlite3
from vkbottle.bot import Blueprint
import pymorphy2


bp = Blueprint("Models")

morph = pymorphy2.MorphAnalyzer()


class User():
    def __init__(self, chat_id: int, user_id: int) -> None:
        self.chat_id = chat_id
        self.user_id = user_id

        if self.user_id < 0:  # Если передана группа, то происходит экранизация класса Group
            self.group = Group(self.user_id)
        else:
            self.group = False

            self.connection = sqlite3.connect("db.db")
            self.cursor = self.connection.cursor()
            if self.check():
                self.cursor.execute(f'''SELECT * FROM users WHERE chat_id = {self.chat_id} AND user_id={self.user_id}''')
                result = self.cursor.fetchone()
                self.messages = result[2]
                self.custom_name = result[3]
                self.sex_request = result[4]

    def check(self, field: str = "user_id") -> int:
        '''
        Проверяет заполнено ли передаваемое поле в БД
        '''
        if self.group == False:  # Проверка на группу
            self.cursor.execute(f'''SELECT {field} FROM users WHERE chat_id = {self.chat_id} AND user_id={self.user_id}''')
            return self.cursor.fetchone()

    def register(self) -> None:
        '''
        Регистрирует нового пользователя
        '''
        if self.group == False:  # Проверка на группу
            self.cursor.execute(f'''INSERT INTO users (chat_id, user_id, messages) VALUES ({self.chat_id}, {self.user_id}, 1)''')
            self.connection.commit()

    def add_message(self) -> None:
        '''
        Добавляет сообщение в статистику
        '''
        if self.group == False:  # Проверка на группу
            self.cursor.execute(f'''UPDATE users SET messages={self.messages+1} WHERE chat_id={self.chat_id} AND user_id={self.user_id}''')
            self.connection.commit()

    async def get_name(self, case: str = "nomn") -> str:
        '''
        Возращает имя юзера в необходимом падеже
        :param case: nomn | gent | datv | accs | ablt | loct | voct
        '''
        if self.group == False:  # Проверка на группу
            if self.custom_name != None:
                raw_name = morph.parse(self.custom_name)[0]
            else:
                vk_info = await bp.api.users.get(self.user_id)
                raw_name = morph.parse(vk_info[0].first_name)[0]
            return raw_name.inflect({case}).word.capitalize()
        else:
            return await self.group.get_name()

    async def get_mention(self, case: str = "nomn") -> str:
        '''
        Возращает упоминания юзера в необходимом падеже
        :param case: nomn | gent | datv | accs | ablt | loct | voct
        '''
        if self.group == False:  # Проверка на группу
            return f"@id{self.user_id} ({await self.get_name(case)})"
        else:
            return await self.group.get_mention()


class Group():
    def __init__(self, group_id: str) -> None:
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

        self.connection = sqlite3.connect("db.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(f'''SELECT * FROM chats WHERE chat_id = {self.chat_id}''')
        result = self.cursor.fetchone()
        if self.check():
            self.owner_id = result[1]
            self.messages = result[2]
            self.last_person_send = result[3]

    def check(self, field: str = "chat_id") -> bool:
        '''
        Проверяет заполнено ли передаваемое поле в БД
        '''
        self.cursor.execute(f'''SELECT {field} FROM chats WHERE chat_id = {self.chat_id}''')
        return self.cursor.fetchone()

    def register(self, owner_id: int):
        '''
        Регистрирует новый чат
        '''
        self.cursor.execute(f'''INSERT INTO chats (chat_id, owner_id, messages) VALUES ({self.chat_id}, {owner_id}, 1)''')
        self.connection.commit()

    def add_message(self):
        '''
        Добавляет сообщение в статистику
        '''
        self.cursor.execute(f'''UPDATE chats SET messages={self.messages+1} WHERE chat_id={self.chat_id}''')
        self.connection.commit()

    def set_last_person_send(self, date) -> None:
        '''
        Обновляет дату последнего использования человека дня
        '''
        self.cursor.execute(f'''UPDATE users SET last_person_send={date} WHERE chat_id={self.chat_id} AND user_id={self.user_id}''')
        self.connection.commit()
