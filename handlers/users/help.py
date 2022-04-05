from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit(5)
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Подписаться на рассылку",
            "/stop - Остановить рассылку",
            "/status - Статус подписки",
            "/help - Получить справку")

    await message.answer("\n".join(text))
