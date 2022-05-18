import sqlite3

connection = sqlite3.connect("db.db")
cursor = connection.cursor()

cursor.execute('''CREATE TABLE "casino_history" (
	"chat_id"	INTEGER,
	"month_year"	INTEGER,
	"day"	INTEGER,
	"win_feature"	TEXT
);''')
connection.commit()
connection.close()
