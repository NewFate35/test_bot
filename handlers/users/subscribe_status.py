from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from keyboards.inline import subscribed, unsubscribed
from loader import dp, db, bot


@dp.message_handler(Command("status"))
async def subscribe_status(message: types.Message):
    user_id = message.from_user.id
    group_member = await bot.get_chat_member(-767464873, user_id)
    if group_member["status"] != "left":
        user = await db.select_user(message.from_user.id)
        if user['status']:
            await message.answer("Вы успешно подписаны на рассылку!", reply_markup=subscribed)
        else:
            await message.answer("Вы не подписаны на рассылку!", reply_markup=unsubscribed)
    else:
        await message.answer(
            "К сожалению, у вас недостаточно прав на использование этого бота. Обратитесь к системному администратору")


@dp.callback_query_handler()
async def subscription_action(call: CallbackQuery):
    user_id = call.from_user.id
    group_member = await bot.get_chat_member(-767464873, user_id)
    if call.data == "subscribe" and group_member["status"] != "left":
        await db.update_user_status(True, user_id)
        await call.message.answer(f"Вы успешно подписались на рассылку, поздравляем!")
    elif call.data == "unsubscribe" and group_member["status"] != "left":
        await db.update_user_status(False, user_id)
        await call.message.answer(f"Вы отписались от рассылки :(")
    else:
        await call.message.answer(
            "К сожалению, у вас недостаточно прав на использование этого бота. Обратитесь к системному администратору")
