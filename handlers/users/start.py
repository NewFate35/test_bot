from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

import asyncpg.exceptions
from loader import dp, bot, db
from utils.misc import rate_limit


@rate_limit(5)
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    group_member = await bot.get_chat_member(-767464873, user_id)
    if group_member["status"] != "left":
        try:
            user = await db.add_user(full_name=message.from_user.full_name, username=message.from_user.username,
                                     telegram_id=message.from_user.id)
        except asyncpg.exceptions.UniqueViolationError:
            user = await db.select_user(telegram_id=message.from_user.id)

        await message.answer(f"Добро пожаловать в Золотое Яблоко!")
    else:
        await message.answer(
            "К сожалению, у вас недостаточно прав на использование этого бота. Обратитесь к системному администратору")
