import nltk
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from Token import TOKEN as token

# Для первого запуска нужно скачать необходимые ресурсы NLTK
nltk.download('punkt')
nltk.download('punkt_tab')

FAQ = {
    "lecture_time": "Лекции проходят по понедельникам и средам с 10:00 до 12:00.",
    "auditorium": "Аудитория находится в корпусе A, кабинет 101.",
    "exam_date": "Экзамен назначен на 15 августа в 14:00.",
    "today_schedule": "Сегодня пар нет. Следующие занятия — завтра с 10:00.",
}

# Ключевые слова для распознавания
KEYWORDS = {
    "lecture_time": ["лекция", "занятия", "урок", "пары"],
    "auditorium": ["аудитория", "кабинет", "комната", "где"],
    "exam_date": ["экзамен", "тест", "контрольная", "когда"],
    "today_schedule": ["сегодня", "расписание", "пар"],
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот о расписании. Задай вопрос, например, 'Когда лекция?'"
    )

def preprocess(text):
    # Токенизация
    tokens = nltk.word_tokenize(text.lower())
    return tokens

def classify_question(tokens):
    # Поиск ключевых слов в тексте
    for category, keywords in KEYWORDS.items():
        for kw in keywords:
            if kw in tokens:
                return category
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    tokens = preprocess(user_text)
    category = classify_question(tokens)
    if category and category in FAQ:
        answer = FAQ[category]
    else:
        answer = "Извини, я не понимаю вопрос. Попробуй переформулировать."
    await update.message.reply_text(answer)

def main():
    TOKEN = token
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот с NLTK запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
