import os
import telebot
from telebot.apihelper import ApiTelegramException
from markups import markups as mp
from dotenv import load_dotenv
import requests

config = load_dotenv()
bot = telebot.TeleBot(os.getenv("TG_API_KEY"))
base_url = os.getenv("base_url")

song_answers = dict()

@bot.message_handler(commands=['start'])
def start(message) -> None:
    try:
        bot.send_message(message.chat.id, mp.start_msg, reply_markup=mp.menu_btn, parse_mode='MARKDOWN')
    except Exception as e:
        bot.reply_to(message, f'{e}')

@bot.message_handler(content_types=["text"])
def text_handler(message):
    try:
        if message.text == 'Найти текст песни 📝':
            msg = bot.send_message(message.chat.id, mp.song1, reply_markup=mp.off_markup, parse_mode='MARKDOWN')
            bot.register_next_step_handler(msg, song1)

        if message.text == 'Об исполнителе 🎵':
            msg = bot.send_message(message.chat.id, mp.actor1, reply_markup=mp.off_markup, parse_mode='MARKDOWN')
            bot.register_next_step_handler(msg, actor1)

    except Exception as e:
        bot.reply_to(message, f'{e}')


def song1(message):
    try:

        song_answers[message.chat.id] = {
            "actor": message.text,
            "song": ''
        }

        msg = bot.send_message(message.chat.id, mp.song2, reply_markup=mp.off_markup, parse_mode='MARKDOWN')
        bot.register_next_step_handler(msg, song2)

    except Exception as e:
        bot.reply_to(message, f'{e}')

def song2(message):
    try:
        song_answers[message.chat.id]['song'] = message.text

        msg_to_delete = bot.send_message(message.chat.id, mp.load, reply_markup=mp.off_markup, parse_mode='MARKDOWN')

        msg_to_delete_id = msg_to_delete.id

        r = requests.post(base_url+'/actor', json={
            "actor": song_answers[message.chat.id]['actor']
        })

        print(r.json())

        r = requests.post(base_url + '/song', json={
            "actor_name": song_answers[message.chat.id]['actor'],
            "songname": song_answers[message.chat.id]['song']
        })

        print(r.json())

        r = requests.get(base_url+'/song/'+str(song_answers[message.chat.id]['song']))

        name_of_song = r.json()['name']
        text_of_song = r.json()['text']

        bot.delete_message(chat_id=message.chat.id, message_id=msg_to_delete_id)

        bot.send_message(message.chat.id, text_of_song, reply_markup=mp.menu_btn, parse_mode='html')

    except ApiTelegramException:
        s1 = text_of_song[:len(text_of_song) // 2]
        s2 = text_of_song[len(text_of_song) // 2:]

        bot.send_message(message.chat.id, s1, reply_markup=mp.menu_btn, parse_mode='html')
        bot.send_message(message.chat.id, s2, reply_markup=mp.menu_btn, parse_mode='html')

    except Exception as e:
        bot.reply_to(message, f'{e}')


def actor1(message):
    try:

        msg_to_delete = bot.send_message(message.chat.id, mp.load, reply_markup=mp.off_markup, parse_mode='MARKDOWN')

        msg_to_delete_id = msg_to_delete.id

        r = requests.post(base_url + '/actor', json={
            "actor": str(message.text)
        })

        print(r.json())

        r = requests.get(base_url + '/actor/' + str(message.text))

        description = r.json()['description']

        bot.delete_message(chat_id=message.chat.id, message_id=msg_to_delete_id)

        bot.send_message(message.chat.id, description, reply_markup=mp.menu_btn, parse_mode='html')

    except ApiTelegramException:
        s1 = description[:len(description) // 2]
        s2 = description[len(description) // 2:]

        bot.send_message(message.chat.id, s1, reply_markup=mp.menu_btn, parse_mode='html')
        bot.send_message(message.chat.id, s2, reply_markup=mp.menu_btn, parse_mode='html')

    except Exception as e:
        bot.reply_to(message, f'{e}')


def main():
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()