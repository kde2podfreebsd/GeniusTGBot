import os
from telebot import types
from dotenv import load_dotenv

config = load_dotenv()
off_markup = types.ReplyKeyboardRemove(selective=False)

start_msg = "*Привет 👋*\nЭтот бот предназначен для поиска *текстов песен* 📝 и *информации об исполнителях!*🎵\n\n_Used API:_ [GeniusAPI](https://docs.genius.com/)"

menu_btn = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
itembtn1 = types.KeyboardButton('Найти текст песни 📝')
itembtn2 = types.KeyboardButton('Об исполнителе 🎵')
menu_btn.add(itembtn1, itembtn2)

song1 = 'Напишите исполнителя/группу'
song2 = 'Напишите название песни'
load = 'Шуршим в бэкенде👀\n\nСмотрим в API Genius и нашу БД'
actor1 = 'Напишите исполнителя/группу'
