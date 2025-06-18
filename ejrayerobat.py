from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

TOKEN = "توکن_ربات_خودت"  # توکن رو داخل متغیر محیطی ذخیره کن

MENU, ENTER_NAME, VERIFY_PHONE, ENTER_NATIONAL_ID = range(4)

def start(update: Update, context: CallbackContext):
    reply_keyboard = [['📝 ثبت‌نام', '💼 اطلاعات من']]
    update.message.reply_text("سلام! لطفاً یکی از گزینه‌ها رو انتخاب کن:", reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
    return MENU

def register(update: Update, context: CallbackContext):
    update.message.reply_text("📝 لطفاً نام و نام خانوادگی خود را وارد کنید:")
    return ENTER_NAME

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={MENU: [MessageHandler(Filters.text & ~Filters.command, register)]},
        fallbacks=[]
    )

    dp.add_handler(conv)
    updater.start_polling()
    print("✅ ربات فعال شد")
    updater.idle()

main()