from datetime import datetime
import re
import sqlite3
from random import choice, randint
from vkbottle.bot import Blueprint
import pymorphy2
from pydantic import BaseModel


# Иниты сюда
bp = Blueprint("Models")
morph = pymorphy2.MorphAnalyzer()


class User():
    def __init__(self, chat_id: int, user_id: int) -> None:
        self.chat_id = chat_id
        self.user_id = user_id

        if self.user_id < 0:
            # Если передана группа,
            # то происходит экранизация класса Group
            self.group = Group(self.user_id)
        else:
            self.group = False

            self.connection = sqlite3.connect("db.db")
            self.cursor = self.connection.cursor()
            # Регистрация юзера во избежания проблем
            if not self.check():
                self.register(0)

            sql = ("SELECT * FROM users WHERE chat_id = :chat_id "
                   "AND user_id = :user_id")
            vars = {"chat_id": self.chat_id,
                    "user_id": self.user_id}

            self.cursor.execute(sql, vars)
            result = self.cursor.fetchone()
            self.messages = result[2]
            self.custom_name = result[3]
            self.sex_request = result[4]
            self.money = result[5] or 0
            self.dick_size = result[6] or 0
            self.last_dick = result[7]
            self.is_admin = result[8] or False
            self.bonus_date = result[9]

    def check(self, field: str = "user_id") -> list[int] | None:
        '''
        Проверяет заполнено ли передаваемое поле в БД
        '''
        if self.group == False:  # Проверка на группу
            sql = ("SELECT :field FROM users WHERE chat_id = :chat_id AND "
                   "user_id = :user_id")
            vars = {"field": field,
                    "chat_id": self.chat_id,
                    "user_id": self.user_id}

            self.cursor.execute(sql, vars)
            return self.cursor.fetchone()

    def register(self, messages_count: int = 1) -> None:
        '''
        Регистрирует нового пользователя
        '''
        if self.group == False:  # Проверка на группу
            sql = ("INSERT INTO users (chat_id, user_id, messages, money) "
                   "VALUES (:chat_id, :user_id, :messages_count, 0)")
            vars = {"chat_id": self.chat_id,
                    "user_id": self.user_id,
                    "messages_count": messages_count}

            self.cursor.execute(sql, vars)
            self.connection.commit()

    def add_message(self) -> None:
        '''
        Добавляет сообщение в статистику
        '''
        if self.group == False:  # Проверка на группу
            sql = ("UPDATE users SET messages = :messages WHERE "
                   "chat_id = :chat_id AND user_id= :user_id")
            vars = {"messages": self.messages + 1,
                    "chat_id": self.chat_id,
                    "user_id": self.user_id}

            self.cursor.execute(sql, vars)
            self.connection.commit()

    def change_money(self, value):
        if self.group == False:  # Проверка на группу
            sql = ("UPDATE users SET money = :money WHERE "
                   "chat_id = :chat_id AND user_id= :user_id")
            vars = {"money": self.money + value,
                    "chat_id": self.chat_id,
                    "user_id": self.user_id}

            self.cursor.execute(sql, vars)
            self.connection.commit()

    async def get_name(self, case: str = "nomn") -> str:
        '''
        Возращает имя юзера в необходимом падеже
        :param case: nomn | gent | datv | accs | ablt | loct | voct
        '''
        if self.group == False:  # Проверка на группу
            if self.custom_name != None:
                raw_name = morph.parse(self.custom_name)[0]
                return raw_name.inflect({case}).word.capitalize()
            else:
                vk_info = await bp.api.users.get(self.user_id)
                try:
                    raw_name = morph.parse(vk_info[0].first_name)[0]
                    return raw_name.inflect({case}).word.capitalize()
                except:
                    return vk_info[0].first_name
        else:
            return await self.group.get_name()

    def test_custom_name(self, name):
        if re.search("^[а-я]+", name.lower()):
            try:
                raw_name = morph.parse(name)[0]
                cases = ["nomn", "gent", "datv",
                         "accs", "ablt", "loct", "voct"]
                for case in cases:
                    raw_name.inflect({case}).word.capitalize()
                return True
            except:
                return "case!"
        else:
            return "words!"

    def set_custom_name(self, name):
        if self.group == False:  # Проверка на группу
            sql = ("UPDATE users SET custom_name = :name WHERE "
                   "chat_id = :chat_id AND user_id = :user_id")
            vars = {"name": name,
                    "chat_id": self.chat_id,
                    "user_id": self.user_id}

            self.cursor.execute(sql, vars)
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

    def update_last_bonus(self, date: int):
        sql = ("UPDATE users SET bonus_date = :date WHERE "
               "chat_id = :chat_id AND user_id = :user_id")
        vars = {"date": date,
                "chat_id": self.chat_id,
                "user_id": self.user_id}

        self.cursor.execute(sql, vars)
        self.connection.commit()

    def change_dick(self, value):
        if self.group == False:  # Проверка на группу
            sql = ("UPDATE users SET dick_size = :size WHERE "
                   "chat_id = :chat_id AND user_id= :user_id")
            vars = {"size": self.dick_size + value,
                    "chat_id": self.chat_id,
                    "user_id": self.user_id}

            self.cursor.execute(sql, vars)
            self.connection.commit()

    def update_last_dick(self, date: int):
        sql = ("UPDATE users SET last_dick = :date WHERE "
               "chat_id = :chat_id AND user_id = :user_id")
        vars = {"date": date,
                "chat_id": self.chat_id,
                "user_id": self.user_id}

        self.cursor.execute(sql, vars)
        self.connection.commit()

    def update_admin(self, value):
        sql = ("UPDATE users SET is_admin = :value WHERE "
               "chat_id = :chat_id AND user_id = :user_id")
        vars = {"value": value,
                "chat_id": self.chat_id,
                "user_id": self.user_id}

        self.cursor.execute(sql, vars)
        self.connection.commit()


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
        sql = "SELECT * FROM chats WHERE chat_id = :chat_id"
        vars = {"chat_id": self.chat_id}

        self.cursor.execute(sql, vars)
        result = self.cursor.fetchone()
        if self.check():
            self.owner_id = result[1]
            self.messages = result[2]
            self.last_person_send = result[3]

    def check(self) -> bool:
        '''
        Проверяет заполнено ли передаваемое поле в БД
        '''
        sql = "SELECT chat_id FROM chats WHERE chat_id = :chat_id"
        vars = {"chat_id": self.chat_id}

        self.cursor.execute(sql, vars)
        return self.cursor.fetchone()

    def register(self, owner_id: int):
        '''
        Регистрирует новый чат
        '''
        sql = ("INSERT INTO chats (chat_id, owner_id, messages) VALUES "
               "(:chat_id, :owner_id, 1)")
        vars = {"chat_id": self.chat_id,
                "owner_id": owner_id}

        self.cursor.execute(sql, vars)
        self.connection.commit()

    def add_message(self):
        '''
        Добавляет сообщение в статистику
        '''
        sql = "UPDATE chats SET messages = :messages WHERE chat_id = :chat_id"
        vars = {"messages": self.messages + 1,
                "chat_id": self.chat_id}

        self.cursor.execute(sql, vars)
        self.connection.commit()

    def set_last_person_send(self, date) -> None:
        '''
        Обновляет дату последнего использования человека дня
        '''
        sql = ("UPDATE chats SET last_person_send = :date WHERE "
               "chat_id = :chat_id")
        vars = {"date": date,
                "chat_id": self.chat_id}

        self.cursor.execute(sql, vars)
        self.connection.commit()

    def get_dicks_top(self) -> list[int] | bool:
        sql = ("SELECT user_id FROM users "
               "WHERE chat_id = :chat_id ORDER BY dick_size DESC")
        vars = {"chat_id": self.chat_id}

        self.cursor.execute(sql, vars)
        return self.cursor.fetchall() or False


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
            if not self.get_alias(i.alias):
                self.add(i.setting, i.alias, i.value)

    def check(self):
        '''
        Проверяет есть ли чат в талице settings
        '''
        sql = "SELECT chat_id FROM settings WHERE chat_id = :chat_id"
        vars = {"chat_id": self.chat_id}

        self.cursor.execute(sql, vars)
        return self.cursor.fetchone()

    def add(self, setting, alias, value):
        setting = setting.lower()
        alias = alias.lower()
        '''
        Добавляет новую настройку
        '''
        sql = ("INSERT INTO settings (chat_id, setting, alias, value) VALUES "
               "(:chat_id, :setting, :alias, :value)")
        vars = {"chat_id": self.chat_id,
                "setting": setting,
                "alias": alias,
                "value": value}

        self.cursor.execute(sql, vars)
        self.connection.commit()

    def get_value(self, alias):
        sql = ("SELECT value FROM settings WHERE "
               "chat_id = :chat_id AND alias = :alias")
        vars = {"chat_id": self.chat_id,
                "alias": alias}

        self.cursor.execute(sql, vars)
        return self.cursor.fetchone()

    def get_alias(self, alias):
        sql = ("SELECT alias FROM settings WHERE "
               "chat_id = :chat_id AND alias = :alias")
        vars = {"chat_id": self.chat_id,
                "alias": alias}

        self.cursor.execute(sql, vars)
        return self.cursor.fetchone()

    def get_all(self):
        '''
        Вовращает все настройки чата
        '''
        sql = "SELECT * FROM settings WHERE chat_id = :chat_id"
        vars = {"chat_id": self.chat_id}

        self.cursor.execute(sql, vars)
        return self.cursor.fetchall()

    def change_value(self, alias):
        alias = alias.lower()
        '''
        Меняет значение value передаваемой настройки на противоположное
        '''
        res = self.get_value(alias)[0]
        if res == "True":
            value = "False"
            value_return = "❌"
        else:
            value = "True"
            value_return = "✅"
        sql = ("UPDATE settings SET value = :value WHERE "
               "chat_id = :chat_id AND alias = :alias")
        vars = {"value": value,
                "chat_id": self.chat_id,
                "alias": alias}

        self.cursor.execute(sql, vars)
        self.connection.commit()
        return value_return

    def get_alias_by_setting(self, setting):
        setting = setting.lower()
        sql = ("SELECT alias FROM settings WHERE chat_id = :chat_id "
               "AND setting = :setting")
        vars = {"chat_id": self.chat_id,
                "setting": setting}

        self.cursor.execute(sql, vars)
        return self.cursor.fetchone()


# TODO: ЗАЩИТА ОТ SQL ИНЪЕКЦИЙ И PEP-8
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


class CasinoUser():
    def __init__(self, chat_id: int, user_id: int) -> None:
        self.chat_id = chat_id
        self.user_id = user_id

        self.connection = sqlite3.connect("db.db")
        self.cursor = self.connection.cursor()

        user_info = self.check()
        if user_info != None:
            self.bet = user_info[2]
            self.feature = user_info[3]

    def check(self) -> list:
        '''
        Проверяет учавствует ли юзер в крутке
        '''
        sql = ("SELECT * FROM casino WHERE chat_id = :chat_id AND "
               "user_id = :user_id")
        vars = {"chat_id": self.chat_id,
                "user_id": self.user_id}
        self.cursor.execute(sql, vars)
        return self.cursor.fetchone()

    def register_bet(self, bet: int, feature: str):
        '''
        Регистрирует пользователя в крутку
        '''
        sql = ("INSERT INTO casino (chat_id, user_id, bet, feature) "
               "VALUES (:chat_id, :user_id, :bet, :feature)")
        vars = {"chat_id": self.chat_id,
                "user_id": self.user_id,
                "bet": bet,
                "feature": feature}

        self.cursor.execute(sql, vars)
        self.connection.commit()


class Casino():
    def __init__(self, chat_id) -> None:
        self.chat_id = chat_id

        self.connection = sqlite3.connect("db.db")
        self.cursor = self.connection.cursor()

    def get_users(self) -> list[tuple[int, int, int, str]]:
        sql = "SELECT * FROM casino WHERE chat_id = :chat_id"
        vars = {"chat_id": self.chat_id}
        self.cursor.execute(sql, vars)
        return self.cursor.fetchall()

    def get_winner_users(self, feature: str) -> list[int]:
        sql = ("SELECT user_id FROM casino WHERE chat_id = :chat_id "
               "AND feature = :feature")
        vars = {"chat_id": self.chat_id,
                "feature": feature}
        self.cursor.execute(sql, vars)
        users = self.cursor.fetchall()
        result = []
        for user in users:
            result.append(user[0])
        return result

    async def get_winner_feature(self) -> str:
        if randint(1, 10) == 1:
            return "🍀"
        return choice(["🔴", "⚫️"])

    def delete_all(self):
        sql = "DELETE FROM casino WHERE chat_id = :chat_id"
        vars = {"chat_id": self.chat_id}
        self.cursor.execute(sql, vars)
        self.connection.commit()

    def add_to_history(self, feature: str):
        now = datetime.now()
        sql = ("INSERT INTO casino_history "
               "(chat_id, date, time, win_feature) VALUES "
               "(:chat_id, :date, :time, :feature)")
        vars = {"chat_id": self.chat_id,
                "date": now.date(),
                "time": str(now.time()),
                "feature": feature}
        self.cursor.execute(sql, vars)
        self.connection.commit()

    def get_history(self) -> list[str] | None:
        now = datetime.now()
        sql = ("SELECT win_feature FROM casino_history WHERE "
               "chat_id = :chat_id AND date = :date LIMIT 20")
        vars = {"chat_id": self.chat_id,
                "date": now.date()}
        self.cursor.execute(sql, vars)
        features = self.cursor.fetchall()
        if features == []:
            return None
        else:
            feature_list = []
            for feature in features:
                feature_list.append(feature[0])
            return feature_list
