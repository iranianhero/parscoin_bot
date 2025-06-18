import sqlite3

# مسیر دیتابیس در Google Colab یا سرور لوکال
DB_PATH = "/content/drive/MyDrive/parscoin.db"

# اتصال به دیتابیس
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# ✅ ایجاد جدول کاربران
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

# ✅ ایجاد جدول تراکنش‌های توکن
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

# 📌 ثبت نمونه داده‌های تستی
def add_user(user_id, full_name, phone, national_id):
    cursor.execute("INSERT INTO users (user_id, full_name, phone, national_id, verified) VALUES (?, ?, ?, ?, ?)",
                   (user_id, full_name, phone, national_id, 1))
    conn.commit()
    print(f"✅ کاربر {full_name} اضافه شد!")

def add_transaction(user_id, amount, status="pending"):
    cursor.execute("INSERT INTO transactions (user_id, amount, status) VALUES (?, ?, ?)",
                   (user_id, amount, status))
    conn.commit()
    print(f"✅ تراکنش {amount} تومان ثبت شد!")

# 📌 تست اولیه دیتابیس
add_user(12345, "علی احمدی", "09123456789", "1234567890")
add_transaction(12345, 10000, "success")

# 📌 بررسی داده‌ها
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

cursor.execute("SELECT * FROM transactions")
print(cursor.fetchall())

conn.close()
print("✅ دیتابیس بسته شد.")