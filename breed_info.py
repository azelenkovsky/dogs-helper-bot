from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import requests
import pickle
from xml.etree import ElementTree as et
import codecs
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import numpy as np
from tabulate import tabulate

#/usr/bin/python3.6
# coding: utf-8
import pandas as pd
import numpy as np
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler,Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import Bot
from telegram.ext import Updater
import datetime
import logging
import time

df = pd.read_csv('check_breeds.csv')

import Levenshtein as lev
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import itertools
import pandas as pd

df = pd.read_csv('check_breeds.csv')
array_of_rus_breeds = df['Название породы (рус)'].to_numpy()



#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, KeyboardButton, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING_FIRST_MENU, TYPING_BREED, TYPING_BREED_KEYBOARD, BREED_FINAL_INFO, BREED_SELECTED_RATING_TOP, DOG_PROFILE_MENU_STEPS, DOG_PROFILE_NICKNAME, DOG_PROFILE_PHOTO, TYPING_REPLY = range(9)

############################################
# all keyboards
############################################

# main menu keyboard
main_menu_reply_keyboard = [
            [KeyboardButton('🐶Все о породе'), KeyboardButton('🔝Рейтинг пород')],
            [KeyboardButton('🤗Мои друзья')],
            [KeyboardButton('📷Фотосессия собаки'), KeyboardButton('🎁Боксы для собак')],
            [KeyboardButton('🦮Изображение собак'), KeyboardButton('📍Приюты')],
            [KeyboardButton('🏠Главное меню')]
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_reply_keyboard, one_time_keyboard=True)


# keyboard for breed info categories
breed_info_reply_keyboard = [
            [KeyboardButton('ℹ️Информация о породе'), KeyboardButton('📊Характеристики породы')],
            [KeyboardButton('История'), KeyboardButton('Описание')],
            [KeyboardButton('Личность'), KeyboardButton('Обучение')],
            [KeyboardButton('Уход'), KeyboardButton('Распространенные заболевания')],
            [KeyboardButton('Стрижка'), KeyboardButton('Полезность')],
            [KeyboardButton('↩️Назад'), KeyboardButton('🏠На главную')]
]

breed_info_markup = ReplyKeyboardMarkup(breed_info_reply_keyboard) #, one_time_keyboard=True)

# keyboard for breed rating categories
breed_rating_reply_keyboard = [
            [KeyboardButton('По Популярности'), KeyboardButton('По Тренировкам')],
            [KeyboardButton('По Размеру'), KeyboardButton('По Разуму')],
            [KeyboardButton('По Охране'), KeyboardButton('По Отношению с детьми')],
            [KeyboardButton('По Ловкости'), KeyboardButton('По Линянию')],
            [KeyboardButton('↩️Назад'), KeyboardButton('🏠На главную')]
]

breed_rating_markup = ReplyKeyboardMarkup(breed_rating_reply_keyboard) #, one_time_keyboard=True)

# keyboard for dog profile
dog_profile_main_menu = [
            [KeyboardButton('🐶Мой профиль')],
            [KeyboardButton('🤗Найти моих друзей!')],
            [KeyboardButton('🦮Иду на прогулку!')],
            [KeyboardButton('↩️Назад'), KeyboardButton('🏠На главную')]
]

dog_profile_main_menu_markup = ReplyKeyboardMarkup(dog_profile_main_menu) #, one_time_keyboard=True)



############################################
# general defs
############################################

def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, value in user_data.items():
        facts.append(f'{key} - {value}')

    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Привет! Я знаю все о собаках и могу помочь Вам во всем. Выберете интересующую вас категорию в меню",
        reply_markup=main_menu_markup,
    )

    return CHOOSING_FIRST_MENU

##########################################
# breed info defs
##########################################
def all_about_breeds_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Введите породу собак, о которой вы хотите узнать:')

    return TYPING_BREED

def all_about_breeds_choice_keyboard(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text

    dict_of_distances = {}

    for i in array_of_rus_breeds:
        match_ratio = fuzz.partial_ratio(text.lower(), i.lower())
        dict_of_distances[i] = match_ratio

    sorted_dict_of_distances = dict(sorted(dict_of_distances.items(), key=lambda x: x[1], reverse=True))
    x = itertools.islice(sorted_dict_of_distances.items(), 0, 10)

    array_of_buttons = []
    for key, value in x:
        if value >= 0.8:
            array_of_buttons.append(key)


    fit_array_of_buttons = []
    for i in array_of_buttons:
        fit_array_of_buttons.append([KeyboardButton(i)])
    breeds_menu = ReplyKeyboardMarkup(fit_array_of_buttons, one_time_keyboard=True)

    update.message.reply_text(
        "Выберете породу из предложенных в меню ниже",
        reply_markup = breeds_menu
    )

    return TYPING_BREED_KEYBOARD

def selected_breed_info_category(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['proper_breed_rus'] = text

    update.message.reply_text(
        "Выберете категорию, которую хотите узнать о выбранной породе",
        reply_markup = breed_info_markup
    )
    print(context.user_data)
    return BREED_FINAL_INFO

def push_breed_info(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['breed_info_category'] = text
    print(context.user_data)

    df_breed = df[df['Название породы (рус)'] == context.user_data['proper_breed_rus']].copy()

    if text == 'ℹ️Информация о породе':
        breed_name_rus = df_breed['Название породы (рус)'].values[0]
        breed_name_eng = df_breed['Название породы (англ)'].values[0]
        breed_country = df_breed['Страна'].values[0]
        breed_lifespan = df_breed['Продолжительность жизни'].values[0]
        breed_height = df_breed['Высота'].values[0]
        breed_weight = df_breed['Вес'].values[0]
        breed_fur_length = df_breed['Длинна шерсти'].values[0]
        breed_colour = df_breed['Цвет'].values[0]
        breed_group = df_breed['Группа'].values[0]
        breed_price = df_breed['Цена'].values[0]

        update.message.reply_text(
            '''
<b>Название породы (рус)</b> - {0}
<b>Название породы (англ)</b> - {1}
<b>Страна</b> - {2}
<b>Продолжительность жизни</b> - {3}
<b>Высота</b> - {4}
<b>Вес</b> - {5}
<b>Длина шерсти</b> - {6}
<b>Цвет</b> - {7}
<b>Группа</b> - {8}
<b>Цена</b> - {9}
            '''.format(breed_name_rus, breed_name_eng, breed_country, breed_lifespan, breed_height, \
                      breed_weight, breed_fur_length, breed_colour, breed_group, breed_price),
            parse_mode=ParseMode.HTML,
            reply_markup = breed_info_markup
        )
    elif text == '📊Характеристики породы':
        breed_name_rus = df_breed['Название породы (рус)'].values[0]
        breed_name_eng = df_breed['Название породы (англ)'].values[0]
        breed_popularity = str(df_breed['Популярность'].values[0])
        breed_training = str(df_breed['Тренировка'].values[0])
        breed_size = str(df_breed['Размер'].values[0])
        breed_intellect = str(df_breed['Разум'].values[0])
        breed_guard = str(df_breed['Охрана'].values[0])
        breed_relations_with_children = str(df_breed['Отношения с детьми'].values[0])
        breed_agility = str(df_breed['Ловкость'].values[0])
        breed_fading = str(df_breed['Линяние'].values[0])

        update.message.reply_text(
            '''
<b>Название породы (рус)</b> - {0}
<b>Название породы (англ)</b> - {1}
<b>Популярность</b> - {2} / 10
<b>Тренировка</b> - {3} / 10
<b>Размер</b> - {4} / 10
<b>Разум</b> - {5} / 10
<b>Охрана</b> - {6} / 10
<b>Отношения с детьми</b> - {7} / 10
<b>Ловкость</b> - {8} / 10
<b>Линяние</b> - {9} / 10
            '''.format(breed_name_rus, breed_name_eng, breed_popularity, breed_training, breed_size, \
                      breed_intellect, breed_guard, breed_relations_with_children, breed_agility, breed_fading),
            parse_mode=ParseMode.HTML,
            reply_markup = breed_info_markup
        )
    elif text == 'История':
        breed_name_rus = df_breed['Название породы (рус)'].values[0]
        breed_name_eng = df_breed['Название породы (англ)'].values[0]
        breed_history = str(df_breed['История'].values[0])

        update.message.reply_text(
            '''
<b>Название породы (рус)</b> - {0}
<b>Название породы (англ)</b> - {1}

<b>История породы</b>
{2}
            '''.format(breed_name_rus, breed_name_eng, breed_history),
            parse_mode=ParseMode.HTML,
            reply_markup = breed_info_markup
        )

    elif text == 'Описание':
        breed_name_rus = df_breed['Название породы (рус)'].values[0]
        breed_name_eng = df_breed['Название породы (англ)'].values[0]
        breed_description = str(df_breed['Описание'].values[0])

        update.message.reply_text(
            '''
<b>Название породы (рус)</b> - {0}
<b>Название породы (англ)</b> - {1}

<b>Описание породы</b>
{2}
            '''.format(breed_name_rus, breed_name_eng, breed_description),
            parse_mode=ParseMode.HTML,
            reply_markup = breed_info_markup
        )

    elif text == 'Личность':
        breed_name_rus = df_breed['Название породы (рус)'].values[0]
        breed_name_eng = df_breed['Название породы (англ)'].values[0]
        breed_personality = str(df_breed['Личность'].values[0])

        update.message.reply_text(
            '''
<b>Название породы (рус)</b> - {0}
<b>Название породы (англ)</b> - {1}

<b>Личность породы</b>
{2}
            '''.format(breed_name_rus, breed_name_eng, breed_personality),
            parse_mode=ParseMode.HTML,
            reply_markup = breed_info_markup
        )

    elif text == 'Обучение':
        breed_name_rus = df_breed['Название породы (рус)'].values[0]
        breed_name_eng = df_breed['Название породы (англ)'].values[0]
        breed_training = str(df_breed['Обучение'].values[0])

        update.message.reply_text(
            '''
<b>Название породы (рус)</b> - {0}
<b>Название породы (англ)</b> - {1}

<b>Обучение породы</b>
{2}
            '''.format(breed_name_rus, breed_name_eng, breed_training),
            parse_mode=ParseMode.HTML,
            reply_markup = breed_info_markup
        )

    elif text == 'Уход':
        breed_name_rus = df_breed['Название породы (рус)'].values[0]
        breed_name_eng = df_breed['Название породы (англ)'].values[0]
        breed_care = str(df_breed['Уход'].values[0])

        update.message.reply_text(
            '''
<b>Название породы (рус)</b> - {0}
<b>Название породы (англ)</b> - {1}

<b>Уход за породой</b>
{2}
            '''.format(breed_name_rus, breed_name_eng, breed_care),
            parse_mode=ParseMode.HTML,
            reply_markup = breed_info_markup
        )

    elif text == 'Распространенные заболевания':
        breed_name_rus = df_breed['Название породы (рус)'].values[0]
        breed_name_eng = df_breed['Название породы (англ)'].values[0]
        breed_diseases = str(df_breed['Распространенные заболевания'].values[0])

        update.message.reply_text(
            '''
<b>Название породы (рус)</b> - {0}
<b>Название породы (англ)</b> - {1}

<b>Распространенные заболевания у породы</b>
{2}
            '''.format(breed_name_rus, breed_name_eng, breed_diseases),
            parse_mode=ParseMode.HTML,
            reply_markup = breed_info_markup
        )

    elif text == 'Стрижка':
        breed_name_rus = df_breed['Название породы (рус)'].values[0]
        breed_name_eng = df_breed['Название породы (англ)'].values[0]
        breed_haircut = str(df_breed['Стрижка'].values[0])

        update.message.reply_text(
            '''
<b>Название породы (рус)</b> - {0}
<b>Название породы (англ)</b> - {1}

<b>Стрижка породы</b>
{2}
            '''.format(breed_name_rus, breed_name_eng, breed_haircut),
            parse_mode=ParseMode.HTML,
            reply_markup = breed_info_markup
        )

    elif text == 'Полезность':
        breed_name_rus = df_breed['Название породы (рус)'].values[0]
        breed_name_eng = df_breed['Название породы (англ)'].values[0]
        breed_usefulness = str(df_breed['Полезность'].values[0])

        update.message.reply_text(
            '''
<b>Название породы (рус)</b> - {0}
<b>Название породы (англ)</b> - {1}

<b>Полезность породы</b>
{2}
            '''.format(breed_name_rus, breed_name_eng, breed_usefulness),
            parse_mode=ParseMode.HTML,
            reply_markup = breed_info_markup
        )

    else:
        update.message.reply_text("Неверная категория", reply_markup = breed_info_markup)

    return BREED_FINAL_INFO

##########################################
# breed rating defs
##########################################

def breed_rating_choose(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['top_category'] = text
    update.message.reply_text(f'Выберите интересующую категорию рейтинга пород в меню:',
        reply_markup = breed_rating_markup)
    return BREED_SELECTED_RATING_TOP

def get_breed_rating_top(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['top_category'] = text

#     print(update.message)
#     print(update)
    print(update.message)
    print(update.message.photo[-1].file_id)
    file_id = update.message.photo[-1].file_id
    newFile = update.message.bot.getFile(file_id)
    newFile.download('dogs_profiles_photos/test.jpg')

    if text == 'По Популярности':
        update.message.bot.send_photo(update.message.chat.id, open('dogs_ratings/Популярность.png','rb'))
    elif text == 'По Тренировкам':
        update.message.bot.send_photo(update.message.chat.id, open('dogs_ratings/Тренировка.png','rb'))
    elif text == 'По Размеру':
        update.message.bot.send_photo(update.message.chat.id, open('dogs_ratings/Размер.png','rb'))
    elif text == 'По Разуму':
        update.message.bot.send_photo(update.message.chat.id, open('dogs_ratings/Разум.png','rb'))
    elif text == 'По Охране':
        update.message.bot.send_photo(update.message.chat.id, open('dogs_ratings/Охрана.png','rb'))
    elif text == 'По Отношению с детьми':
        update.message.bot.send_photo(update.message.chat.id, open('dogs_ratings/Отношения с детьми.png','rb'))
    elif text == 'По Ловкости':
        update.message.bot.send_photo(update.message.chat.id, open('dogs_ratings/Ловкость.png','rb'))
    elif text == 'По Линянию':
        update.message.bot.send_photo(update.message.chat.id, open('dogs_ratings/Линяние.png','rb'))
    else:
        update.message.reply_text('Неверная категория')

    return BREED_SELECTED_RATING_TOP

##########################################
# breed social network defs
##########################################

def dog_social_network(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['sn_category'] = text
    update.message.reply_text(f'Выберите интересующую Вас категорию профиля в меню:',
        reply_markup = dog_profile_main_menu_markup)
    return DOG_PROFILE_MENU_STEPS

def dog_print_get_nickname(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['previous_category'] = text
    print()
    update.message.reply_text(f'Введите Кличку вашей собаки')

    return DOG_PROFILE_NICKNAME

def dog_print_get_photo(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    date = update.message.date
    chat_id = update.message.chat.id
    username = update.message.chat.username
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name

    context.user_data['username'] = username
    context.user_data['first_name'] = first_name
    context.user_data['last_name'] = last_name
    context.user_data['chat_id'] = chat_id
    context.user_data['date'] = date
    context.user_data['dog_nickname'] = text
    print(update.message)
    update.message.reply_text(f'Пришлите нам фото вашей собаки')

    return DOG_PROFILE_PHOTO

def dog_get_all_data_received(update: Update, context: CallbackContext) -> int:
#    user_data = context.user_data
#     text = update.message.text
#     chat_id = update.message.chat.id
#     username = update.message.chat.username
#     first_name = update.message.chat.first_name
#     last_name = update.message.chat.last_name
#     user_data['chat_id'] = chat_id
#     user_data['dog_nickname'] = text
#    del user_data['dog_profile_choice']
    context.user_data['photo_id'] = update.message.photo[-1].file_id
    print(context.user_data)

    update.message.reply_text(
        "Отлично! Ниже информация, которую Вы мне рассказали:"
        f"{facts_to_str(context.user_data)} Расскажите еще о вашей собаке"
        " on something."
    )

    file_id = update.message.photo[-1].file_id
    newFile = update.message.bot.getFile(file_id)
    newFile.download('dogs_profiles_photos/terra.jpg')

    update.message.reply_text("Вы загрузили фото вашей собаки в соцсеть")

    return DOG_PROFILE_NICKNAME

##########################################
# test location defs
##########################################

def location_test(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['menu_title'] = text

    update.message.bot.sendLocation(update.message.chat.id, 55.744606, 37.733347)
    update.message.bot.sendLocation(update.message.chat.id, 55.746551, 37.731383)

    return CHOOSING_FIRST_MENU

#    bot.send_photo(chat_id=chat_id, photo=open('tests/test.png', 'rb'))

# def keyboard_of_proper_breeds(update: Update, context: CallbackContext) -> int:



# ##### example def-s
def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Your {text.lower()}? Yes, I would love to hear about that!')

    return TYPING_REPLY


def custom_choice(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Alright, please send me the category first, ' 'for example "Most impressive skill"'
    )

    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)} You can tell me more, or change your opinion"
        " on something.",
        reply_markup=main_menu_markup,
    )

    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)} Until next time!"
    )

    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("your_telegram_bot_token_here", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            # состояние главного меню
            CHOOSING_FIRST_MENU: [
                # handler to run all about breeds
                MessageHandler(
                    Filters.regex('^(🐶Все о породе)$'), all_about_breeds_choice
                ),
                MessageHandler(
                    Filters.regex('^(🔝Рейтинг пород)$'), breed_rating_choose
                ),
                MessageHandler(
                    Filters.regex('^(🤗Мои друзья)$'), dog_social_network
                ),
                MessageHandler(
                    Filters.regex('^(📍Приюты)$'), location_test
                )
            ],

            # состояния меню "Информация о породе"
            TYPING_BREED: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), all_about_breeds_choice_keyboard,
                )
            ],

            TYPING_BREED_KEYBOARD: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), selected_breed_info_category,
                )
            ],

            BREED_FINAL_INFO: [
                MessageHandler(
                    Filters.regex('^(ℹ️Информация о породе|📊Характеристики породы|История|Описание|Личность|Обучение|Уход|Распространенные заболевания|Стрижка|Полезность)$'), push_breed_info
                ),
                MessageHandler(Filters.regex('^(↩️Назад)$'), all_about_breeds_choice),
                MessageHandler(Filters.regex('^(🏠На главную)$'), start),
            ],

            # состояния меню "Топ пород собак"
            BREED_SELECTED_RATING_TOP: [
                MessageHandler(
                    Filters.regex('^(По Популярности|По Тренировкам|По Размеру|По Разуму|По Охране|По Отношению с детьми|По Ловкости|По Линянию)$'), get_breed_rating_top
                ),
#               MessageHandler(Filters.photo, get_breed_rating_top),
#               update.message.photo[-1].file_id
                MessageHandler(Filters.regex('^(↩️Назад)$'), start),
                MessageHandler(Filters.regex('^(🏠На главную)$'), start),
            ],

            # Состояние меню "Мой профиль"
            DOG_PROFILE_MENU_STEPS: [
                MessageHandler(Filters.regex('^(🐶Мой профиль)$'), dog_print_get_nickname)
            ],

            DOG_PROFILE_NICKNAME: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), dog_print_get_photo,
                )
            ],

            DOG_PROFILE_PHOTO: [
                MessageHandler(Filters.photo, dog_get_all_data_received)
            ],

            # Другое
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
