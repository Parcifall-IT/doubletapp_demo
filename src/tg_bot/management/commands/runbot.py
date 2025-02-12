from django.core.management.base import BaseCommand
from tg_bot.bot import run_bot  # Импортируем функцию запуска бота


class Command(BaseCommand):
    help = "Запускает Telegram-бота"

    def handle(self, *args, **kwargs):
        run_bot()
