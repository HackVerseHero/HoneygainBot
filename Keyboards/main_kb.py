from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_board = ReplyKeyboardMarkup(resize_keyboard=True)
open_honeypot_button = KeyboardButton("Open honeypot 🍯")
get_status_button = KeyboardButton("Get status 🪄")
get_statistics_button = KeyboardButton("Get statistics 📊")
main_board.row(open_honeypot_button).row(get_status_button, get_statistics_button)
