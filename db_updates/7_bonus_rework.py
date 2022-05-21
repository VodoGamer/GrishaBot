import sqlite3

connection = sqlite3.connect("db.db")
cursor = connection.cursor()


cursor.execute("ALTER TABLE users DROP last_bonus;")
cursor.execute("ALTER TABLE users ADD bonus_date TEXT;")


connection.commit()
connection.close()
