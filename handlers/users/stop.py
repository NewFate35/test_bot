from aiogram import types

from loader import dp, db, bot
from utils.misc import rate_limit


@rate_limit(5)
@dp.message_handler(commands=['stop'])
async def bot_stop(message: types.Message):
    user_id = message.from_user.id
    group_member = await bot.get_chat_member(-767464873, user_id)
    if group_member["status"] != "left":
        await db.update_user_status(new_status=False, telegram_id=message.from_user.id)
        await message.answer(f"До свидания! С наилучшими пожеланиями, Золотое Яблоко!")
    else:
        await message.answer(
            "К сожалению, у вас недостаточно прав на использование этого бота. Обратитесь к системному администратору")
