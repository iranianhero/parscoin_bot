import sqlite3

DB_PATH = "/content/drive/MyDrive/parscoin.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# جدول کاربران
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    full_name TEXT,
    phone TEXT,
    national_id TEXT,
    verified INTEGER DEFAULT 0
)
""")

# جدول تراکنش‌ها
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount INTEGER,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
print("✅ دیتابیس و جداول با موفقیت ایجاد شدند!")
conn.close()