import sqlite3

# инициализация базы данных
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            role TEXT NOT NULL,
            telegram_user_id INTEGER UNIQUE,
            first_name TEXT NOT NULL,
            username TEXT,
            last_name TEXT,
            language_code TEXT,
            ai_enabled BOOLEAN DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


# проверка существования пользователя в базе данных
def user_exists(telegram_user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_user_id = ?", (telegram_user_id,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# проверка на доступ к чату
def is_chat_accessible(chat_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_user_id = ? AND ai_enabled = ?", (chat_id, 1,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# выдать права администратора
def admin_add(user_id):
    if user_exists(user_id):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET ai_enabled = 1, role = 'admin' WHERE telegram_user_id = ?",
            (user_id,)
        )
        conn.commit()
        conn.close()
        return True
    return False

# сохранение пользователя при первом контакте
def save_user(from_user):
    if not user_exists(from_user.id):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (role, telegram_user_id, first_name, username, last_name, language_code) VALUES (?, ?, ?, ?, ?, ?)",
            ('user', from_user.id, from_user.first_name, from_user.username, from_user.last_name, from_user.language_code)
        )
        conn.commit()
        conn.close()


# cursor.execute("SELECT * FROM users")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)