import sqlite3

connection = sqlite3.connect("template.db")
cursor = connection.cursor()


cursor.execute('''DROP TABLE casino_history''')
cursor.execute(
    '''CREATE TABLE "casino_history" (
        "chat_id"	INTEGER,
        "date"	TEXT,
        "time"  TEXT,
        "win_feature"	TEXT
    )'''
)
connection.commit()
connection.close()
