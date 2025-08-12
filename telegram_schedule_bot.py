import nltk
from telegram import Update
from datetime import datetime, timedelta, timezone
import os.path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from Token import TOKEN as token

# Для первого запуска нужно скачать необходимые ресурсы NLTK
nltk.download('punkt')
nltk.download('punkt_tab')

# --- Google Calendar API setup ---
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDS_FILENAME = 'creditionalsthree.json'
TOKEN_FILENAME = 'token.json'

def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILENAME):
        creds = Credentials.from_authorized_user_file(TOKEN_FILENAME, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILENAME, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILENAME, 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

# --- Ответы FAQ ---
FAQ = {
    "lecture_time": "Лекции проходят по понедельникам и средам с 10:00 до 12:00.",
    "auditorium": "Аудитория находится в корпусе A, кабинет 101.",
    "exam_date": "Экзамен назначен на 15 августа в 14:00.",
    "today_schedule": "Сегодня пар нет. Следующие занятия — завтра с 10:00.",
}

KEYWORDS = {
    "lecture_time": ["лекция", "занятия", "урок", "пары"],
    "auditorium": ["аудитория", "кабинет", "комната", "где"],
    "exam_date": ["экзамен", "тест", "контрольная", "когда"],
    "today_schedule": ["сегодня", "расписание", "пар"],
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот о расписании. Задай вопрос или напиши /reminders для списка ближайших дедлайнов."
    )

def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    return tokens

def classify_question(tokens):
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

async def reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = get_calendar_service()

    now = datetime.now(timezone.utc).isoformat()
    week_later = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=week_later,
        maxResults=5,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        reply = "Ближайших дедлайнов в календаре нет."
    else:
        reply = "Ближайшие дедлайны:\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # Преобразуем дату в удобочитаемый формат
            try:
                dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                start_str = dt.strftime('%d.%m.%Y %H:%M')
            except Exception:
                start_str = start
            summary = event.get('summary', '(без названия)')
            reply += f"- {summary} {start_str}\n"

    await update.message.reply_text(reply)

def main():
    TOKEN = token
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reminders", reminders))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот с интеграцией Google Calendar запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()