import random

import pandas as pd
from aiogram import executor

from loader import dp, db, scheduler
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

wishes = pd.read_excel(r'Добрые пожелания.xlsx', sheet_name='Лист1').values


async def send_message_at_time():
    users = await db.select_all_users()
    for user in users:
        random_phrase = "".join(random.choice(wishes))
        await dp.bot.send_message(chat_id=user['telegram_id'], text=random_phrase)


def schedule_jobs():
    scheduler.add_job(send_message_at_time, "cron", hour='12', timezone="Europe/Moscow")


async def on_startup(dispatcher):
    await db.create()
    await db.create_table_users()

    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    schedule_jobs()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
