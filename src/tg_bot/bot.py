import os
import django
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = settings.TELEGRAM_BOT_TOKEN


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Я Telegram-бот, работающий через Django!")


async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)


def run_bot():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Бот запущен...")
    app.run_polling()
