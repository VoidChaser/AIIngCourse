# import asyncio
# import json
# from dotenv import load_dotenv
# load_dotenv()  # загружает переменные из .env в os.environ
# import logging
# import os
# from datetime import datetime, timedelta, timezone
#
# import nltk
# from telegram import Update
# from telegram.ext import (
#     ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
# )
#
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
#
# from intent import SemanticFAQ, keyword_fallback
#
# # --- Логи ---
# logging.basicConfig(
#     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
#     level=logging.INFO
# )
# logger = logging.getLogger("ai_schedule_bot")
#
# # --- NLTK ресурсы (без punkt_tab) ---
# nltk.download("punkt", quiet=True)
#
# # --- Google Calendar ---
# SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
# CREDS_FILENAME = os.environ.get("GOOGLE_CREDENTIALS", "credentials.json")
# TOKEN_FILENAME = os.environ.get("GOOGLE_TOKEN_FILE", "token.json")
#
# def get_calendar_service():
#     creds = None
#     if os.path.exists(TOKEN_FILENAME):
#         creds = Credentials.from_authorized_user_file(TOKEN_FILENAME, SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             logger.info("Refreshing Google token...")
#             creds.refresh(Request())
#         else:
#             logger.info("Launching OAuth flow for Google...")
#             flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILENAME, SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open(TOKEN_FILENAME, "w") as token:
#             token.write(creds.to_json())
#             logger.info("Google token stored in %s", TOKEN_FILENAME)
#     return build("calendar", "v3", credentials=creds)
#
# # --- Семантическая база знаний ---
# faq = SemanticFAQ()  # лениво загрузится при первом вопросе
#
# HELP_TEXT = (
#     "Привет! Я бот курса 📚\n\n"
#     "Я умею:\n"
#     "• Отвечать на вопросы о расписании, аудиториях, дедлайнах, экзаменах\n"
#     "• Искать смысловой ответ по базе знаний (даже если вопрос сформулирован «по-человечески»)\n"
#     "• Показывать ближайшие дедлайны из Google Calendar: /reminders\n\n"
#     "Попробуй спросить: «когда лекция?», «где проходит занятие?», «когда дедлайн проекта?»"
# )
#
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(HELP_TEXT)
#
# async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(HELP_TEXT)
#
# async def reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         service = get_calendar_service()
#         now = datetime.now(timezone.utc).isoformat()
#         week_later = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
#
#         events_result = service.events().list(
#             calendarId="primary",
#             timeMin=now,
#             timeMax=week_later,
#             maxResults=10,
#             singleEvents=True,
#             orderBy="startTime"
#         ).execute()
#         events = events_result.get("items", [])
#
#         if not events:
#             reply = "Ближайших дедлайнов в календаре нет."
#         else:
#             lines = ["Ближайшие дедлайны:"]
#             for event in events:
#                 start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
#                 summary = event.get("summary", "(без названия)")
#                 try:
#                     # Приводим к локальному времени пользователя (Европа/Хельсинки ~ UTC+2/+3)
#                     dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
#                     local = dt.astimezone()  # системный TZ контейнера/хоста
#                     start_str = local.strftime("%d.%m.%Y %H:%M")
#                 except Exception:
#                     start_str = start
#                 lines.append(f"• {summary} — {start_str}")
#             reply = "\n".join(lines)
#         await update.message.reply_text(reply)
#     except Exception as e:
#         logger.exception("reminders failed: %s", e)
#         await update.message.reply_text("Не удалось получить события из Google Calendar. Проверь авторизацию и файл credentials.json.")
#
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = (update.message.text or "").strip()
#     if not text:
#         return
#
#     # 1) сначала быстрый фоллбек по ключевым словам
#     kw = keyword_fallback(text)
#     if kw:
#         await update.message.reply_text(kw)
#         return
#
#     # 2) затем пробуем семантический ответ
#     try:
#         ans, score = faq.search(text, top_k=1)
#         # порог уверенности
#         if score >= 0.45:
#             await update.message.reply_text(ans)
#         else:
#             await update.message.reply_text("Я не уверен, что правильно понял вопрос. Уточни формулировку или попробуй /reminders для ближайших дедлайнов.")
#     except Exception as e:
#         logger.warning("semantic search failed, fallback. err=%s", e)
#         await update.message.reply_text("Пока не могу обработать этот вопрос. Попробуй задать по-другому или используй /reminders.")
#
# def main():
#     token = os.environ.get("TELEGRAM_TOKEN")
#     if not token:
#         raise RuntimeError("Не задан TELEGRAM_TOKEN в .env или переменных окружения")
#
#     app = ApplicationBuilder().token(token).build()
#
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("help", help_cmd))
#     app.add_handler(CommandHandler("reminders", reminders))
#     app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
#
#     logger.info("Bot is up. Waiting for messages...")
#     app.run_polling()
#
# if __name__ == "__main__":
#     main()
import os
import logging
from datetime import datetime, timedelta, timezone

import nltk
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- Отключаем предупреждения Hugging Face (Windows) ---
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_XET_WARNING"] = "1"

from intent import SemanticFAQ, keyword_fallback

# --- Логи ---
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("ai_schedule_bot")

# --- NLTK ресурсы ---
nltk.download("punkt", quiet=True)

# --- Google Calendar ---
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CREDS_FILENAME = os.environ.get("GOOGLE_CREDENTIALS", "credentials.json")
TOKEN_FILENAME = os.environ.get("GOOGLE_TOKEN_FILE", "token.json")


def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILENAME):
        creds = Credentials.from_authorized_user_file(TOKEN_FILENAME, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing Google token...")
            creds.refresh(Request())
        else:
            logger.info("Launching OAuth flow for Google...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILENAME, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILENAME, "w") as token:
            token.write(creds.to_json())
            logger.info("Google token stored in %s", TOKEN_FILENAME)
    return build("calendar", "v3", credentials=creds)


# --- Загружаем модель сразу при старте (не лениво) ---
logger.info("Loading SemanticFAQ model...")
faq = SemanticFAQ()  # модель загружается сразу, бот не зависнет на первом сообщении
logger.info("Model loaded!")


HELP_TEXT = (
    "Привет! Я бот курса 📚\n\n"
    "Я умею:\n"
    "• Отвечать на вопросы о расписании, аудиториях, дедлайнах, экзаменах\n"
    "• Искать смысловой ответ по базе знаний (даже если вопрос сформулирован «по-человечески»)\n"
    "• Показывать ближайшие дедлайны из Google Calendar: /reminders\n\n"
    "Попробуй спросить: «когда лекция?», «где проходит занятие?», «когда дедлайн проекта?»"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)


async def reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        service = get_calendar_service()
        now = datetime.now(timezone.utc).isoformat()
        week_later = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            timeMax=week_later,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])

        if not events:
            reply = "Ближайших дедлайнов в календаре нет."
        else:
            lines = ["Ближайшие дедлайны:"]
            for event in events:
                start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
                summary = event.get("summary", "(без названия)")
                try:
                    dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                    local = dt.astimezone()
                    start_str = local.strftime("%d.%m.%Y %H:%M")
                except Exception:
                    start_str = start
                lines.append(f"• {summary} — {start_str}")
            reply = "\n".join(lines)
        await update.message.reply_text(reply)
    except Exception as e:
        logger.exception("reminders failed: %s", e)
        await update.message.reply_text(
            "Не удалось получить события из Google Calendar. Проверь авторизацию и файл credentials.json."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if not text:
        return

    # Быстрый фоллбек по ключевым словам
    kw = keyword_fallback(text)
    if kw:
        await update.message.reply_text(kw)
        return

    # Семантический ответ
    try:
        ans, score = faq.search(text, top_k=1)
        if score >= 0.45:
            await update.message.reply_text(ans)
        else:
            await update.message.reply_text(
                "Я не уверен, что правильно понял вопрос. Уточни формулировку или попробуй /reminders."
            )
    except Exception as e:
        logger.warning("semantic search failed, fallback. err=%s", e)
        await update.message.reply_text(
            "Пока не могу обработать этот вопрос. Попробуй задать по-другому или используй /reminders."
        )


def main():
    from dotenv import load_dotenv

    load_dotenv()  # загружаем .env в os.environ

    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("Не задан TELEGRAM_TOKEN в .env или переменных окружения")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("reminders", reminders))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logger.info("Bot is up. Waiting for messages...")
    app.run_polling()


if __name__ == "__main__":
    main()

# import os
# import logging
# from datetime import datetime
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
#
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from google.auth.transport.requests import Request
#
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch
# from dotenv import load_dotenv
#
# # Загружаем переменные окружения
# load_dotenv()
# TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
#
# # Настраиваем логирование
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
#
# # Настройки Google Calendar
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# CREDENTIALS_FILE = 'credentials.json'
#
#
# def get_calendar_service():
#     creds = None
#     if os.path.exists(CREDENTIALS_FILE):
#         creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     service = build('calendar', 'v3', credentials=creds)
#     return service
#
#
# # Загружаем модель RuGPT
# MODEL_NAME = "sberbank-ai/rugpt3small_based_on_gpt2"
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
#
#
# def generate_rugpt_response(question: str) -> str:
#     """Генерация ответа с помощью RuGPT."""
#     input_ids = tokenizer.encode(question, return_tensors="pt")
#     output_ids = model.generate(
#         input_ids,
#         max_length=200,
#         do_sample=True,
#         top_p=0.95,
#         top_k=50,
#         temperature=0.8,
#         pad_token_id=tokenizer.eos_token_id
#     )
#     response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
#     return response
#
#
# # Обработчики команд
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "Привет! Я учебный бот RuGPT. Помогаю с учебными вопросами и показываю твои события из Google Calendar."
#     )
#
#
# async def reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     service = get_calendar_service()
#     now = datetime.utcnow().isoformat() + 'Z'
#     events_result = service.events().list(
#         calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime'
#     ).execute()
#     events = events_result.get('items', [])
#
#     if not events:
#         await update.message.reply_text("Событий нет.")
#         return
#
#     reply = "Твои ближайшие события:\n"
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         reply += f"- {event['summary']} ({start})\n"
#
#     await update.message.reply_text(reply)
#
#
# async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     question = update.message.text
#     response = generate_rugpt_response(question)
#     await update.message.reply_text(response)
#
#
# # Запуск бота
# def main():
#     app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
#
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("reminders", reminders))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_question))
#
#     print("Бот запущен...")
#     app.run_polling()
#
#
# if __name__ == "__main__":
#     main()
