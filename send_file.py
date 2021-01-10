# !/usr/bin/env python
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
#import database

import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
users = []

logger = logging.getLogger(__name__)

ADMIN_CHECKING1,ADMIN_CHECKING, SEND_PHOTO,  SEND_CHECK, send_check_to_admin, ASK_PHOTO, GENDER, PHOTO, SURNAME, RU, HEIGHT, AGE, SPECIALITY, INCOME, INSTA, BIO, CHECK, SEARCHING, SEARCHING1 = range(
    19)

questions_kaz = ["Фотоңызды жіберіңіз", "Жыңысынызды жіберіңіз", "Аты-жөніңізді жіберіңіз", "Руыңызды жіюеріңіз",
                 "Бойыңызды жіберіңіз", "Кім болып жұмыс жасайсыз?", "Айлық табысыңыз қанша?",
                 "Инстаграмдагы аккаунтыңызды жіберіңіз", "Өзіңіз жайлы қысқаша ақпарат"]
question_rus = ["Отправьте фото", "Напишите ваш пол", "Напишите имя фамилию", "Напишите ваш ру", "Напишите ваш рост",
                "Напишите кем вы работаете", "Напишите ваш ежемесячный доход", "Напишите ваш аккаунт в инстаграм",
                "Опишите себя в пару предложений"]
users_1 = []
users_2 = []

updater = Updater("1415351884:AAHmLW6l-z6vLqVIHtw-KwzomMydkel6MZw", use_context=True)
#425471123 = Diana

def start(update: Update, context: CallbackContext) -> int:
    if update.message.chat_id == 140340457:
        update.message.reply_text(
            'Для того чтобы подтвердить когда придет чек нажмите кнопку подтвердить'
        )
        print('admiiiiiiiin')
        return ADMIN_CHECKING
    else:
        update.message.reply_text(
            'Отправьте чек Каспи'
        )

        return SEND_CHECK


def send_check(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    check_file = update.message.photo[-1].get_file()
    check_file.download('{}_check_photo.jpg'.format(user.first_name))

    logger.info("check_photo of %s: %s", user.first_name, 'check_photo.jpg')
    update.message.reply_text('Ожидайте пароль')

    # bot.send_photo(chat_id=chat_id, photo=open('tests/test.png', 'rb'))

    return send_check_to_admin(update, context, user)


def admin_checking(update: Update, context: CallbackContext) -> int:
    global users
    if update.message.chat_id == 140340457:
        if update.message.text[:11] == 'Подтвердить'  and len(str(update.message.text)) == 25:
            reply_keyboard = [['Начать регистрацию'],['Отправить чек сначала']]
            chat_id = update.message.text[16:]
            users.append(chat_id)
            updater.bot.send_message(text="Вам был открыт доступ пожайлуста нажмите кнопку начать регистрацию", chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return ADMIN_CHECKING1
        elif update.message.text[:15] == 'Не подтверждать' and len(str(update.message.text)) == 29:
            chat_id = update.message.text[20:]
            reply_keyboard = [['Отправить чек сначала']]
            updater.bot.send_message(text="Ваш чек не был подтвержден пожайлуста отправьте чек еще раз", chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ADMIN_CHECKING1
    else:
         if update.message.text == 'Начать регистрацию':
             if 1 == 1:
                    return send_photo(update, context)
             else:
                reply_keyboard = [['Начать регистрацию'],['Отправить чек сначала']]
                updater.bot.send_message(text="Ваш чек не был подтвержден пожайлуста попробуйте позже или нажмите отправьте чек еще раз", chat_id=update.message.chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                return ADMIN_CHECKING1
         else:
             return start(update, context)

def admin_checking1(update: Update, context: CallbackContext) -> int:
    global users
    if update.message.chat_id == 140340457:
        if update.message.text[:11] == 'Подтвердить'  and len(str(update.message.text)) == 25:
            reply_keyboard = [['Начать регистрацию'],['Отправить чек сначала']]
            chat_id = update.message.text[16:]
            updater.bot.send_message(text="Вам был открыт доступ пожайлуста нажмите кнопку начать регистрацию", chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            users.append(chat_id)
            return ADMIN_CHECKING
        elif update.message.text[:15] == 'Не подтверждать' and len(str(update.message.text)) == 29:
            chat_id = update.message.text[20:]
            reply_keyboard = [['Отправить чек сначала']]
            updater.bot.send_message(text="Ваш чек не был подтвержден пожайлуста отправьте чек еще раз", chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ADMIN_CHECKING
    else:
        if update.message.text == "Начать регистрацию":
            if 1 == 1:
                return send_photo(update, context)
            else:
                reply_keyboard = [['Начать регистрацию'],['Отправить чек сначала']]
                updater.bot.send_message(text="Ваш чек не был подтвержден пожайлуста попробуйте позже или нажмите отправьте чек еще раз", chat_id=update.message.chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                return ADMIN_CHECKING
        else:
            return start(update, context)

''''
def start(update: Update, context: CallbackContext) -> int:
    if update.message.chat_id == 42547112399:
        update.message.reply_text(
        'Admiiiin'
        )
        return ADMIN_CHECK
    else:
        update.message.reply_text(
            'Отправьте чек Каспи'
        )
        return SEND_CHECK


def send_check(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    check_file = update.message.photo[-1].get_file()
    check_file.download('/Users/a22807/Desktop/love_is_photos/{}_check_photo.jpg'.format(user.first_name))

    logger.info("check_photo of %s: %s", user.first_name, 'check_photo.jpg')
    update.message.reply_text('Ожидайте пароль')

    # bot.send_photo(chat_id=chat_id, photo=open('tests/test.png', 'rb'))

    return send_check_to_admin(update, context, user)
'''

def send_check_to_admin(update: Update, context: CallbackContext, user) -> int:
    # get chat id with admin and then use it
    chat_id="140340457"
    #diana_chat_id = update.message.chat.id
    #print(diana_chat_id)
    updater.bot.send_photo(chat_id=chat_id, photo=open('{}_check_photo.jpg'.format(user.first_name), 'rb'))
    reply_keyboard = [['Подтвердить чек '+str(update.message.chat_id)], ['Не подтверждать чек '+str(update.message.chat_id)]]
    updater.bot.send_message(text=update.message.chat_id, chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ADMIN_CHECKING

def send_photo(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Отправьте ваше фото'
    )
    return PHOTO

'''
def admin_check(update: Update, context: CallbackContext) -> int:
    if update.message.chat_id == 425471123:
        if update.message.text == 'ДА':
            return admin_check(update,context)
        else:
            return START'''

def photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    context.user_data["photofile"] = photo_file
    photo_file.download('user_photo.jpg')
    context.user_data["photo"] = "path to photo"
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    reply_keyboard = [['Мужчина', 'Женщина']]
    update.message.reply_text(
        'Выберите ваш пол',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return GENDER



def gender(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    gender = update.message.text
    context.user_data["gender"]=gender
    update.message.reply_text(
        'Напишите ваше имя и фамилию',
        reply_markup=ReplyKeyboardRemove(),
    )

    return SURNAME


def surname(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("FIO of %s: %s", user.first_name, update.message.text)
    surname = update.message.text
    context.user_data["surname"]=surname
    update.message.reply_text('Напишите ваш ру')

    return RU


def ru(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Ru of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Напишите ваш рост')
    ru = update.message.text
    context.user_data["ru"]=ru

    return HEIGHT


def height(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Height of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Напишите ваш вес')
    height = update.message.text
    context.user_data["height"]=height
    return AGE


def age(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Weight of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Напишите кем вы работаете')
    age = update.message.text
    context.user_data["age"]=age

    return SPECIALITY


def speciality(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Speciality of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Напишите ваш ежемесячный доход')
    speciality = update.message.text
    context.user_data["speciality"]=speciality

    return INCOME


def income(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Income of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Напишите ваш аккаунт в инстаграм')
    income = update.message.text
    context.user_data["income"]=income

    return INSTA


def insta(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Insta of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Опишите себя в пару предложений')
    insta = update.message.text
    context.user_data["insta"]=insta
    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)

    bio = update.message.text
    context.user_data["bio"]=bio
    print(context.user_data)
    reply_keyboard = [['Правильно', 'Редактировать']]
    updater.bot.send_photo(chat_id=update.message.chat_id, photo=open('user_photo.jpg', 'rb'), caption='\n2. '+context.user_data["gender"]+'\n3. '+context.user_data["surname"]+'\n4. '+context.user_data["ru"]+'\n5. '+context.user_data["height"]+'\n6. '+context.user_data["age"]+'\n7. '+context.user_data["speciality"]+'\n8. '+context.user_data["income"]+'\n9. '+context.user_data["insta"]+'\n10. '+context.user_data["bio"])
    update.message.reply_text('Спасибо что заполнили пожайлуста посмотрите и проверьте',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
    return CHECK


def check(update: Update, context: CallbackContext) -> int:
    print("user information", context.user_data)
    user_data = context.user_data
    #database.add(user_data["gender"], user_data["photo"], user_data["age"], user_data["surname"], user_data["surname"], user_data["ru"], user_data["height"], user_data["speciality"], user_data["income"], user_data["insta"], user_data["bio"], update.message.chat_id)
    #database.add_chat_gender(update.message.chat_id,user_data["gender"] )
    #database.show_parthers(update.message.chat_id)

    user = update.message.from_user
    if update.message.text == 'Правильно':
        reply_keyboard = [['1', '2', '3', '4', '5', 'Дальше', 'Закрыть']]
        update.message.reply_text('Выберите:\n'
                                  '1. Diana Omarova\n'
                                  '2. Assiya Zhamelova\n'
                                  '3. Linara Omarova\n'
                                  '4. Amina Myrzagalieva\n'
                                  '5. Altynay Kulnazarova\n'
                                  'Дальше\n'
                                  'Закрыть'
                                  , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                     resize_keyboard=True), )
        return SEARCHING

    else:
        update.message.reply_text('Спасибо что заполнили')

        return SEARCHING


def searching(update: Update, context: CallbackContext) -> int:
    print("yyyyyy")

    #database.show_parthers(update.message.chat_id)

    #print("for shahmar", database.show_parthers(update.message.chat_id))

    if update.message.text == 'Дальше':

        reply_keyboard = [['6', '7', '8', '9', '10', 'Дальше', 'Назад', 'Закрыть']]
        update.message.reply_text('Выберите:\n'
                                  '6. Alinur Mukhmaedzhanova\n'
                                  '7. Aydana Shalkar\n'
                                  '8. Ayzhan Nesipbay\n'
                                  '9. Dayan Tezekbaeva\n'
                                  '10. Saule Kalenova\n'
                                  'Дальше\n'
                                  'Назад\n'
                                  'Закрыть\n'
                                  , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                     resize_keyboard=True), )
        return SEARCHING1
    elif update.message.text == 'Закрыть':
        return ConversationHandler.END


def searching1(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Like', 'Назад', 'Закрыть']]
    update.message.reply_text(
        '2. Женщина\n'
        '3. Aydana Shalkar\n'
        '4. Найман\n'
        '5. 170\n'
        '6. 55\n'
        '7. оператор в кселл\n'
        '8. 150 000\n'
        '9. aydana_shalkar\n'
        '10. Скромная и стеснительная девушка\n'
        , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'До свидание дорогой друг!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1415351884:AAHmLW6l-z6vLqVIHtw-KwzomMydkel6MZw", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            #ADMIN_CHECK: [MessageHandler(Filters.text & ~Filters.command, admin_check)],
            send_check_to_admin: [MessageHandler(Filters.photo, send_check_to_admin)],
            SEND_CHECK: [MessageHandler(Filters.photo, send_check)],
            PHOTO: [MessageHandler(Filters.photo, photo)],
            GENDER: [MessageHandler(Filters.regex('^(Мужчина|Женщина)$'), gender)],
            SURNAME: [MessageHandler(Filters.text & ~Filters.command, surname)],
            RU: [MessageHandler(Filters.text & ~Filters.command, ru)],
            HEIGHT: [MessageHandler(Filters.text & ~Filters.command, height)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, age)],
            SPECIALITY: [MessageHandler(Filters.text & ~Filters.command, speciality)],
            INCOME: [MessageHandler(Filters.text & ~Filters.command, income)],
            INSTA: [MessageHandler(Filters.text & ~Filters.command, insta)],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
            CHECK: [MessageHandler(Filters.regex('^(Правильно|Редактировать)$'), check)],
            SEARCHING: [MessageHandler(Filters.text & ~Filters.command, searching)],
            SEARCHING1: [MessageHandler(Filters.text & ~Filters.command, searching1)],
            SEND_PHOTO: [MessageHandler(Filters.photo, send_photo)],
            ADMIN_CHECKING: [MessageHandler(Filters.text & ~Filters.command, admin_checking)],
            ADMIN_CHECKING1: [MessageHandler(Filters.text & ~Filters.command, admin_checking1)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
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
