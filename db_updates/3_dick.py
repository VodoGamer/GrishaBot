import sqlite3

connection = sqlite3.connect("db.db")
cursor = connection.cursor()

cursor.execute('''ALTER TABLE users ADD COLUMN dick_size INT;''')
cursor.execute('''ALTER TABLE users ADD COLUMN last_dick INT;''')
connection.commit()
connection.close()
