import os
import django
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from django.conf import settings
from .models import AppAdminuser
from django.contrib.auth.hashers import make_password
from asgiref.sync import sync_to_async
from django.utils.timezone import now
import re


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = settings.TELEGRAM_BOT_TOKEN


async def create_or_get_user(user_id, username, first_name, last_name):
    return await sync_to_async(AppAdminuser.objects.get_or_create)(
        username=username,
        defaults={
            'password': make_password(None),
            'first_name': first_name or '',
            'last_name': last_name or '',
            'email': f'{username}@example.com',
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
            'date_joined': now(),
            'phone_number': None,
        }
    )


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username or f'user_{user_id}'
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    email = f'{username}@example.com'

    user, created = await create_or_get_user(user_id, username, first_name, last_name)

    message = "Вы успешно зарегистрированы! Введите /set_phone <номер> для завершения регистрации." if created \
        else "Вы уже зарегистрированы. Введите /set_phone <номер>, если ещё не указали его."

    await update.message.reply_text(message)


async def get_user(username):
    return await sync_to_async(AppAdminuser.objects.filter(username=username).first)()


async def set_phone(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username or f'user_{user_id}'
    user = await get_user(username)

    if not user:
        await update.message.reply_text("Сначала введите /start для регистрации.")
        return

    if context.args:
        phone_number = context.args[0]
        user.phone_number = phone_number
        await sync_to_async(user.save)()
        await update.message.reply_text(f"Номер {phone_number} сохранён!")
    else:
        await update.message.reply_text(
            "Введите номер телефона после команды /set_phone: \nПример: `/set_phone 89001234567`")


async def restricted_command(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = await get_user(user_id)

    if user and user.phone_number:
        await update.message.reply_text("Эта ком,анда пока недоступна.")
    else:
        await update.message.reply_text("Сначала укажите свой номер телефона командой /set_phone.")


def escape_markdown_v2(text):
    if text is None:
        return "—"
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', str(text))


async def me(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username or f'user_{user_id}'
    user = await get_user(username)

    if not user:
        await update.message.reply_text("Сначала введите /start для регистрации.")
        return

    user_info = (
        f"👤 *Ваш профиль*\n"
        f"🆔 ID: `{escape_markdown_v2(user_id)}`\n"
        f"👤 Логин: `{escape_markdown_v2(user.username)}`\n"
        f"📛 Имя: {escape_markdown_v2(user.first_name)}\n"
        f"🏷 Фамилия: {escape_markdown_v2(user.last_name)}\n"
        f"📧 Email: `{escape_markdown_v2(user.email)}`\n"
        f"📱 Телефон: `{escape_markdown_v2(user.phone_number)}`\n"
        f"📅 Дата регистрации: `{escape_markdown_v2(user.date_joined.strftime('%Y-%m-%d %H:%M:%S'))}`\n"
    )

    await update.message.reply_text(user_info, parse_mode="MarkdownV2")


def run_bot():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set_phone", set_phone))
    app.add_handler(CommandHandler("me", me))

    app.add_handler(MessageHandler(filters.COMMAND, restricted_command))

    logger.info("Бот запущен...")
    app.run_polling()
