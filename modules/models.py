import sqlite3
from vkbottle.bot import Blueprint
import pymorphy2
from pydantic import BaseModel


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

    def set_custom_name(self, name):
        if self.group == False:  # Проверка на группу
            self.cursor.execute(f'''UPDATE users SET custom_name="{name}" WHERE chat_id={self.chat_id} AND user_id={self.user_id}''')
            self.connection.commit()

    async def get_mention(self, case: str = "nomn") -> str:
        '''
        Возращает упоминания юзера в необходимом падеже
        :param case: nomn | gent | datv | accs | ablt | loct | voct
        '''
        if self.group == False:  # Проверка на группу
            return f"@id{self.user_id} ({await self.get_name(case)})"
        else:
            return await self.group.get_mention()

    async def get_sex(self):
        '''
        Возвращает пол пользователя.\n
        1 - девушка\n
        0 - парень
        '''
        if self.group == False:  # Проверка на группу
            return (await bp.api.users.get(self.user_id, "sex"))[0].sex.value


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
        self.cursor.execute(f'''UPDATE chats SET last_person_send={date} WHERE chat_id={self.chat_id}''')
        self.connection.commit()


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

        self.connection = sqlite3.connect("db.db")
        self.cursor = self.connection.cursor()

    def update(self):
        for i in default_settings.settings:
            if not self.get("alias", i.alias):
                self.add(i.setting, i.alias, i.value)

    def check(self):
        '''
        Проверяет есть ли чат в талице settings
        '''
        self.cursor.execute(f'''SELECT chat_id FROM settings WHERE chat_id={self.chat_id}''')
        return self.cursor.fetchone()

    def add(self, setting, alias, value):
        setting = setting.lower()
        alias = alias.lower()
        '''
        Добавляет новую настройку
        '''
        self.cursor.execute(f'''INSERT INTO settings (chat_id, setting, alias, value) VALUES ({self.chat_id}, "{setting}", "{alias}", "{value}")''')
        self.connection.commit()

    def get(self, field, alias):
        field = field.lower()
        alias = alias.lower()
        '''
        Возвращает поле определённой настройки
        '''
        self.cursor.execute(f'''SELECT "{field}" FROM settings WHERE chat_id={self.chat_id} AND alias="{alias}"''')
        return self.cursor.fetchone()

    def get_all(self):
        '''
        Вовращает все настройки чата
        '''
        self.cursor.execute(f'''SELECT * FROM settings WHERE chat_id={self.chat_id}''')
        return self.cursor.fetchall()

    def change_value(self, alias):
        alias = alias.lower()
        '''
        Меняет значение value передаваемой настройки на противоположное
        '''
        res = self.get("value", alias)[0]
        if res == "True":
            value = "False"
            value_return = "❌"
        else:
            value = "True"
            value_return = "✅"
        self.cursor.execute(f'''UPDATE settings SET value="{value}" WHERE chat_id={self.chat_id} AND alias="{alias}"''')
        self.connection.commit()
        return value_return

    def get_alias_by_setting(self, setting):
        setting = setting.lower()
        self.cursor.execute(f'''SELECT "alias" FROM settings WHERE chat_id={self.chat_id} AND setting="{setting}"''')
        return self.cursor.fetchone()


class Sex():
    def __init__(self, chat_id: int, from_user: int) -> None:
        self.chat_id = chat_id
        self.from_user = from_user

        self.connection = sqlite3.connect("db.db")
        self.cursor = self.connection.cursor()

    def start(self, to_id) -> None:
        '''
        "from_user" предлогает секс переданному юзеру
        '''
        self.cursor.execute(f'''UPDATE users SET sex_request={self.from_user} WHERE chat_id={self.chat_id} AND user_id={to_id}''')
        self.connection.commit()

    def get_request(self) -> None | int:
        '''
        есть ли запрос на секс у "from_user" от другого юзера
        возвращает id другого юзера
        '''
        self.cursor.execute(
            f'''SELECT sex_request FROM users WHERE chat_id={self.chat_id} AND user_id={self.from_user}''')
        result = self.cursor.fetchone()
        if result is None: return None
        else: return result[0]

    def get_send(self) -> None | int:
        '''
        отправлял ли "from_user" запрос на секс другому
        возращает id другого юзера
        '''
        self.cursor.execute(f'''SELECT user_id FROM users WHERE chat_id={self.chat_id} AND sex_request={self.from_user}''')
        result = self.cursor.fetchone()
        if result is None: return None
        else: return result[0]

    def end_sex(self, to_id):
        '''
        убирает заявку на секс отправленную от "from_user"
        '''
        self.cursor.execute(f'''UPDATE users SET sex_request=Null WHERE chat_id={self.chat_id} AND user_id={to_id}''')
        self.connection.commit()

    def discard_sex(self):
        '''
        отклонение предложения секса от другого юзера "from_user"
        '''
        self.cursor.execute(f'''UPDATE users SET sex_request=Null WHERE chat_id={self.chat_id} AND user_id={self.from_user}''')
        self.connection.commit()
