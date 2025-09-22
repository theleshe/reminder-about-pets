import os
import asyncio
import logging
from datetime import time
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список напоминаний
reminders = [
    (time(7, 30), "Доброе утро! Ставь реакцию на напоминания - если выполнил дела с животными! Это очень важно!"),
    (time(8, 0), "Нужно: 1. Погулять с Милой и покормить ее 2. Выдать фосфалюгель 0.5мл Алисе"),
    (time(8, 30), "Кормить Алиску! Не забудь Псиллиум. + Энтерол, если пришло время"),
    (time(9, 0), "Эспумизан беби Алиске надо!"),
    (time(14, 0), "С Милой погулять надо!"),
    (time(15, 0), "Фосфалюгель Алиске 0.5мл!"),
    (time(16, 0), "1. Кормить Алиску! На забудь Псиллиум. + Энтерол, если пришло время 2. Марфлоксин 1мл, Преднифарм 0.5табл"),
    (time(17, 0), "Эспумизан беби Алиске надо!"),
    (time(18, 30), "Фосфалюгель Алиске 0.5мл!"),
    (time(19, 0), "1. Кормить Алиску! Не забудь Псиллиум. 2. Погулять с Милой и покормить ее"),
    (time(20, 0), "Надо обработать швы Алиске!")
]

async def send_reminder(text: str):
    logger.info(f"Отправляю напоминание: {text}")
    await bot.send_message(CHAT_ID, text)

def setup_scheduler():
    scheduler = AsyncIOScheduler(timezone="Europe/Astrakhan")
    for reminder_time, text in reminders:
        logger.info(f"📌 Добавлено напоминание: {reminder_time} -> {text}")
        scheduler.add_job(
            send_reminder,
            "cron",
            hour=reminder_time.hour,
            minute=reminder_time.minute,
            args=[text]
        )
    scheduler.start()

async def main():
    await bot.send_message(CHAT_ID, "✅ Бот запущен и работает!")
    setup_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
