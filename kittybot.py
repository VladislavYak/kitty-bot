from asyncio.log import logger
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
import requests
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

# setting up logginng
load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('my_logger.log', maxBytes=50000000, backupCount=5)
logger.addHandler(handler)

# some constant values init
SECRET_TOKEN = os.getenv('KITTY_BOT_TOKEN')
URL = 'https://api.thecatapi.com/v1/images/search'
BUTTON = 'Получить котика'

def start(update, context):
    chat = update.effective_chat
    
    logging.info(f'Somebody has used /start command. Username: {chat.username}')

    keyboard = [
        [
            KeyboardButton(BUTTON, callback_data="/kitty"),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


    hello_text = f"""Привет, это бот с котиками
Нажми кнопку ниже, чтобы получить котика"""

    context.bot.send_message(chat_id=chat.id, text=hello_text,
     reply_markup=reply_markup, parse_mode='Markdown')


def buttonHandler(update, context):
    chat = update.effective_chat
    if button in update.message.text:
        link = get_kitty_pic()
        context.bot.send_photo(update.effective_chat.id, link)
    else:
       context.bot.send_message(chat_id=chat.id, text='Я умею только котиков отправлять')

def get_kitty_pic():
    try:
        r = requests.get(url=URL)
    except Exception as e:
        logger.exception(f'Got api error: {e}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        r = requests.get(new_url)

    r = r.json()
    random_cat = r[0].get('url')
    return random_cat

def main():
    updater = Updater(token=SECRET_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, buttonHandler))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    logger.info('Starting KittyBot')
    main()