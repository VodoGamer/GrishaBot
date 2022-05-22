import sqlite3

connection = sqlite3.connect("db.db")
cursor = connection.cursor()


cursor.execute("SELECT chat_id, user_id FROM users")
users = []
for i in cursor.fetchall():
    users.append(i)
for user in users:
    print(user)
    vars = {'chat_id': user[0],
            'user_id': user[1]}
    cursor.execute("UPDATE users SET bonus_date = Null WHERE "
                   "chat_id = :chat_id AND user_id = :user_id", vars)


connection.commit()
connection.close()
