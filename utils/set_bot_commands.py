from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Подписаться на рассылку"),
            types.BotCommand("stop", "Остановить рассылку"),
            types.BotCommand("status", "Статус подписки"),
            types.BotCommand("help", "Вывести справку"),
        ]
    )
