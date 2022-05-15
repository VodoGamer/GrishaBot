import sqlite3

connection = sqlite3.connect("db.db")
cursor = connection.cursor()

cursor.execute('''CREATE TABLE "casino" (
	"chat_id"	INTEGER,
	"user_id"	INTEGER,
	"bet"	INTEGER,
	"feature"	TEXT
);''')
cursor.execute('''ALTER TABLE users ADD COLUMN money INT;''')
connection.commit()
connection.close()
