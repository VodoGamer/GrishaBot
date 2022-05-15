import sqlite3

connection = sqlite3.connect("db.db")
cursor = connection.cursor()

cursor.execute('''ALTER TABLE users ADD COLUMN last_bonus INT;''')
connection.commit()
connection.close()
