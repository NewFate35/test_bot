from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

subscribed = InlineKeyboardMarkup(row_width=1)
unsubscribe_button = InlineKeyboardButton('Отписаться', callback_data='unsubscribe')
subscribed.add(unsubscribe_button)


unsubscribed = InlineKeyboardMarkup(row_width=1)
subscribe_button = InlineKeyboardButton('Подписаться', callback_data='subscribe')
unsubscribed.add(subscribe_button)
