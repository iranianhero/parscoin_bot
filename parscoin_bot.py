import sqlite3
import random
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

TOKEN = os.getenv("TOKEN")  # بهتره توکن از متغیر محیطی خوانده بشه
DB_PATH = "/content/drive/MyDrive/parscoin.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# ایجاد جدول کاربران با نام و نام خانوادگی
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
conn.commit()

MENU, ENTER_NAME, VERIFY_PHONE, ENTER_NATIONAL_ID = range(4)

def start(update: Update, context: CallbackContext):
    reply_keyboard = [['📝 ثبت‌نام', '💼 اطلاعات من']]
    update.message.reply_text(
        "سلام! لطفاً یکی از گزینه‌ها رو انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )
    return MENU

def register(update: Update, context: CallbackContext):
    update.message.reply_text("📝 لطفاً نام و نام خانوادگی خود را وارد کنید:")
    return ENTER_NAME

def enter_name(update: Update, context: CallbackContext):
    full_name = update.message.text.strip()
    context.user_data["full_name"] = full_name
    update.message.reply_text("📞 لطفاً شماره تلفن خود را وارد کنید:")
    return VERIFY_PHONE

def verify_phone(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    phone = update.message.text.strip()
    code = random.randint(1000, 9999)  

    context.user_data["phone"] = phone
    context.user_data["verification_code"] = code

    update.message.reply_text(f"🔢 کد تأیید شما: {code} (فعلاً پیامک واقعی نیست)")
    update.message.reply_text("✏️ لطفاً کد تأیید را وارد کنید:")
    return ENTER_NATIONAL_ID

def enter_national_id(update: Update, context: CallbackContext):
    code_entered = update.message.text.strip()
    correct_code = context.user_data.get("verification_code")

    if code_entered != str(correct_code):
        update.message.reply_text("❌ کد اشتباه است. لطفاً دوباره امتحان کن.")
        return VERIFY_PHONE

    update.message.reply_text("🆔 لطفاً کد ملی خود را وارد کنید:")
    return MENU

def menu_handler(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.effective_user.id
    full_name = context.user_data.get("full_name")
    phone = context.user_data.get("phone")
    national_id = text.strip()

    cursor.execute("INSERT INTO users (user_id, full_name, phone, national_id, verified) VALUES (?, ?, ?, ?, ?)",
                   (user_id, full_name, phone, national_id, 1))
    conn.commit()

    update.message.reply_text(f"✅ ثبت‌نام کامل شد!\n👤 نام: {full_name}\n📞 شماره: {phone}\n🆔 کد ملی: {national_id}")
    return MENU

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [MessageHandler(Filters.text & ~Filters.command, menu_handler)],
            ENTER_NAME: [MessageHandler(Filters.text & ~Filters.command, enter_name)],
            VERIFY_PHONE: [MessageHandler(Filters.text & ~Filters.command, verify_phone)],
            ENTER_NATIONAL_ID: [MessageHandler(Filters.text & ~Filters.command, enter_national_id)]
        },
        fallbacks=[]
    )

    dp.add_handler(conv)
    updater.start_polling()
    print("✅ ربات فعال شد")
    updater.idle()

main()
