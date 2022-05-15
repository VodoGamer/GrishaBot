import sqlite3

connection = sqlite3.connect("db.db")
cursor = connection.cursor()

cursor.execute('''ALTER TABLE users ADD COLUMN is_admin TEXT;''')
connection.commit()
connection.close()
