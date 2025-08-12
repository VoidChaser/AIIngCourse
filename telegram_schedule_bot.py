from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Предопределённые ответы на вопросы о расписании
FAQ = {
    "Когда лекция?": "Лекции проходят по понедельникам и средам с 10:00 до 12:00.",
    "Где аудитория?": "Аудитория находится в корпусе A, кабинет 101.",
    "Когда экзамен?": "Экзамен назначен на 15 августа в 14:00.",
    "Расписание на сегодня": "Сегодня пар нет. Следующие занятия — завтра с 10:00.",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот о расписании. Задай вопрос, например, 'Когда лекция?'"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    answer = FAQ.get(user_text, "Извини, я не знаю ответа на этот вопрос.")
    await update.message.reply_text(answer)

def main():
    # Вставьте сюда свой токен, полученный у @BotFather
    TOKEN = "7315764780:AAG7-A-VpZsOXBm_o7ZUos4kvYWtHwkRaWA"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
