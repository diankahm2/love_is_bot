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
import database
import logging
import random

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
updater = Updater("1415351884:AAHmLW6l-z6vLqVIHtw-KwzomMydkel6MZw", use_context=True)

logger = logging.getLogger(__name__)

EDITING, EDITING_PHOTO, EDITING_TEXT, SEND_CHECK, send_check_to_admin, ASK_PHOTO, GENDER, PHOTO, SURNAME, RU, HEIGHT, AGE, SPECIALITY, INCOME, INSTA, BIO, CHECK, SEARCHING, SEARCHING1, SEND_PHOTO, ADMIN_CHECKING, ADMIN_CHECKING1 = range(22)

users = []
users_male=database.show_parthers_male()
#users_male=[(1, 'Мужчина', 'path to photo', 'ruslan', 'ruslan', 'tt', 'tt', 'tt', 'tt', 'tt', 'tt', 'rr', '425471123', '0'), (2, 'Мужчина', 'path to photo', 'hh', 'hh', 'tt', 'gg', 'ff', 'uu', 'jj', 'ii', 'kk', '425471123', '0'), (3, 'Мужчина', 'path to photo', 'll', 'll', 'jj', 'kk', 'kk', 'jj', 'jj', 'kk', 'kk', '425471123', '0'), (4, 'Мужчина', 'path to photo', 'dd', 'dd', 'ddd', 'ddd', 'ddd', 'ddd', 'sss', 'ddd', 'ddd', '425471123', '0'), (5, 'Мужчина', 'path to photo', 'asa', 'asa', 'asas', 'sas', 'asas', 'asas', 'asas', 'asa', 'asas', '425471123', '0')]
print("MALES", users_male[0:5])

users_female=database.show_parthers_female()
#users_female=[(1, 'Женщина', 'path to photo', 'Kamila', 'Kamila', 'Aa', 'Aa', 'Aa', 'Aa', 'Aa', 'Aa', 'Aa', '426352620', '0'), (2, 'Женщина', 'path to photo', 'Kamila', 'Kamila', 'Ddd', 'Aa', 'Aaa', 'Ffff', 'Jj', 'Ggg', 'Kk', '426352620', '0'), (3, 'Женщина', 'path to photo', 'Kamila', 'Kamila', 'Ddd', 'Aaa', 'Aaa', 'Jjj', 'Kk', 'Ggg', 'Pp', '426352620', '0'), (4, 'Женщина', 'path to photo', 'Diana', 'Diana', 'Aa', 'Aa', 'Aa', 'Aa', 'Aa', 'Aa', 'Aa', '425471123', '0'), (5, 'Женщина', 'path to photo', 'll', 'll', 'hh', 'kk', 'kk', 'hh', 'ii', 'oo', 'pp', '425471123', '0')]
print("FEMALES", users_female[0:5])

def start(update: Update, context: CallbackContext) -> int:
    context.user_data["viewer"] = 0
    print(type(context.user_data["viewer"]))
    if update.message.chat_id == 425471123:
        update.message.reply_text(
            'Для того чтобы подтвердить когда придет чек нажмите кнопку подтвердить'
        )
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
    print(update.message.text[:11])
    print(len(str(update.message.text)))
    if update.message.chat_id == 425471123:
        #if update.message.text[:11] == 'Подтвердить' and len(str(update.message.text)) == 25:
        if update.message.text[:11] == 'Подтвердить':
            reply_keyboard = [['Начать регистрацию'],['Отправить чек сначала']]
            chat_id = update.message.text[16:]
            updater.bot.send_message(text="Вам был открыт доступ пожайлуста нажмите кнопку начать регистрацию", chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            users.append(chat_id)
            
            return ADMIN_CHECKING1
        elif update.message.text[:15] == 'Не подтверждать':
            #and len(str(update.message.text)) == 29
            chat_id = update.message.text[20:]
            reply_keyboard = [['Отправить чек сначала']]
            updater.bot.send_message(text="Ваш чек не был подтвержден пожайлуста отправьте чек еще раз", chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            users.append(chat_id)
            return ADMIN_CHECKING1
    else:
        if update.message.text == "Начать регистрацию":
            if str(update.message.chat_id) in users:
                return send_photo(update, context)
            else:
                reply_keyboard = [['Начать регистрацию'],['Отправить чек сначала']]
                updater.bot.send_message(text="Ваш чек не был подтвержден пожайлуста попробуйте позже или нажмите отправьте чек еще раз", chat_id=update.message.chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                return ADMIN_CHECKING1
        else:
            return start(update, context)
# shaha 140340457
def admin_checking1(update: Update, context: CallbackContext) -> int:
    if update.message.chat_id == 425471123:
        print(update.message.text[:11])
        if update.message.text[:11] == 'Подтвердить' and len(str(update.message.text)) == 25:
            reply_keyboard = [['Начать регистрацию'],['Отправить чек сначала']]
            chat_id = update.message.text[16:]
            updater.bot.send_message(text="Вам был открыт доступ пожайлуста нажмите кнопку начать регистрацию", chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            users.append(chat_id)
            
            return ADMIN_CHECKING1
        elif update.message.text[:15] == 'Не подтверждать' and len(str(update.message.text)) == 29:
            chat_id = update.message.text[20:]
            reply_keyboard = [['Отправить чек сначала']]
            updater.bot.send_message(text="Ваш чек не был подтвержден пожайлуста отправьте чек еще раз", chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            users.append(chat_id)
            return ADMIN_CHECKING1
    else:
        if update.message.text == "Начать регистрацию":
            if str(update.message.chat_id) in users:
                return send_photo(update, context)
            else:
                reply_keyboard = [['Начать регистрацию'],['Отправить чек сначала']]
                updater.bot.send_message(text="Ваш чек не был подтвержден пожайлуста попробуйте позже или нажмите отправьте чек еще раз", chat_id=update.message.chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                return ADMIN_CHECKING
        else:
            return start(update, context)
            
    
    
def send_check_to_admin(update: Update, context: CallbackContext, user) -> int:
    # get chat id with admin and then use it
    chat_id="425471123"
    #diana_chat_id = update.message.chat.id
    #print(diana_chat_id)
    updater.bot.send_photo(chat_id=chat_id, photo=open('{}_check_photo.jpg'.format(user.first_name), 'rb'))
    reply_keyboard = [['Подтвердить чек '+str(update.message.chat_id)], ['Не подтверждать чек '+str(update.message.chat_id)]]
    #reply_keyboard = [['Подтвердить'], ['Не подтверждать']]

    updater.bot.send_message(text=update.message.chat_id, chat_id=chat_id, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ADMIN_CHECKING

def send_photo(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Отправьте ваше фото', reply_markup=ReplyKeyboardRemove()
    )
    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    path_to_photo = "/Users/a22807/Desktop/love_is_photos/photos/%s.jpg"% (user.first_name+str(random.randint(0, 10000000)))
    photo_file.download(path_to_photo)
    logger.info("Photo of %s: %s", user.first_name, 'path_to_photo')

    context.user_data["editing"] = 0
    context.user_data["path_to_photo"] = path_to_photo
    
    reply_keyboard = [['Мужчина', 'Женщина']]
    update.message.reply_text(
        'Выберите ваш пол',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return GENDER



def gender(update: Update, context: CallbackContext) -> int:

    '''print("1", context.user_data["viewer"]) #0
    print("2", type(users_male[0]))
    print("3", users_male[context.user_data["viewer"]][1])
    print("4", users_male[context.user_data["viewer"]][4])

    #print("5", (context.user_data["viewer"])[1])'''
    #updater.bot.send_message(text="Вас лайкнул %s можете его тоже лайкнуть" % (context.user_data["surname"]), chat_id=chat_id_towrite)

   
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    gender = update.message.text
    context.user_data["gender"]=gender
    
    if context.user_data["editing"] == 1:
        
        return bio(update,context)
    else:
    
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
    
    if context.user_data["editing"] == 1:
        return bio(update,context)
    else:
        update.message.reply_text('Напишите ваш ру')
        return RU


def ru(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Ru of %s: %s", user.first_name, update.message.text)
    
    ru = update.message.text
    context.user_data["ru"]=ru
    if context.user_data["editing"] == 1:
        return bio(update,context)
    else:
        update.message.reply_text('Напишите ваш рост')
        return HEIGHT


def height(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Height of %s: %s", user.first_name, update.message.text)
    height = update.message.text
    context.user_data["height"]=height
    if context.user_data["editing"] == 1:
        return bio(update,context)
    else:
        update.message.reply_text('Напишите ваш вес')
        return AGE


def age(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Weight of %s: %s", user.first_name, update.message.text)
    age = update.message.text
    context.user_data["age"]=age
    if context.user_data["editing"] == 1:
        return bio(update,context)
    else:
        update.message.reply_text('Напишите кем вы работаете')
        return SPECIALITY


def speciality(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Speciality of %s: %s", user.first_name, update.message.text)
    speciality = update.message.text
    context.user_data["speciality"]=speciality
    if context.user_data["editing"] == 1:
        return bio(update,context)
    else:
        update.message.reply_text('Напишите ваш ежемесячный доход')
        return INCOME


def income(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Income of %s: %s", user.first_name, update.message.text)
    income = update.message.text
    context.user_data["income"]=income
    if context.user_data["editing"] == 1:
        return bio(update,context)
    else:
        update.message.reply_text('Напишите ваш аккаунт в инстаграм')
        return INSTA


def insta(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Insta of %s: %s", user.first_name, update.message.text)
    insta = update.message.text
    context.user_data["insta"]=insta
    if context.user_data["editing"] == 1:
        return bio(update,context)
    else:
        update.message.reply_text('Опишите себя в пару предложений')
        return BIO


def bio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    if context.user_data["editing"] == 2 or context.user_data["editing"] == 0:
        bio = update.message.text
        context.user_data["bio"]=bio
    reply_keyboard = [['Правильно', 'Редактировать']]
    updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(context.user_data["path_to_photo"], 'rb'), caption='\n2. '+context.user_data["gender"]+'\n3. '+context.user_data["surname"]+'\n4. '+context.user_data["ru"]+'\n5. '+context.user_data["height"]+'\n6. '+context.user_data["age"]+'\n7. '+context.user_data["speciality"]+'\n8. '+context.user_data["income"]+'\n9. '+context.user_data["insta"]+'\n10. '+context.user_data["bio"])
    update.message.reply_text('Спасибо что заполнили пожайлуста посмотрите и проверьте',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
    return CHECK


def check(update: Update, context: CallbackContext) -> int:
    #print("user information", context.user_data)
    #photo_path="fix it"
    user_data = context.user_data
    print(user_data["path_to_photo"])
    database.add(user_data["gender"], user_data["path_to_photo"], user_data["age"], user_data["surname"], user_data["surname"], user_data["ru"], user_data["height"], user_data["speciality"], user_data["income"], user_data["insta"], user_data["bio"], update.message.chat_id)
    database.add_chat_gender(update.message.chat_id,user_data["gender"])
    #database.show_parthers(update.message.chat_id)
    #print("pathers to show", database.show_parthers(update.message.chat_id))
    user = update.message.from_user
    if update.message.text == 'Правильно': #kogda najmet' pravil'no nujno napisat' if exist potomu chto redaktirovanie toje zdes' proidet tak chot nujno napisat' kak to
        # users_male i users_female zdes' nujno pomenyat'
        users.remove(str(update.message.chat_id))
        reply_keyboard = [['Назад', 'Like', 'Следующий']]
        
        if context.user_data["gender"] == 'Мужчина':
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"][2]], 'rb'), caption='\n2.'+users_female[context.user_data["viewer"][1]]+'\n3.'+users_female[context.user_data["viewer"][3]]+'\n4. '+users_female[context.user_data["viewer"][4]]+'\n5. '+users_female[context.user_data["viewer"][5]]+'\n6. '+users_female[context.user_data["viewer"][6]]+'\n7. '+users_female[context.user_data["viewer"][7]]+'\n8. '+users_female[context.user_data["viewer"][8]]+'\n9. '+users_female[context.user_data["viewer"][9]]+'\n10. '+users_female[context.user_data["viewer"][10]], reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"]][1]+'\n3. '+users_female[context.user_data["viewer"]][3]+'\n4. '+users_female[context.user_data["viewer"]][4]+'\n5. '+users_female[context.user_data["viewer"]][5]+'\n6. '+users_female[context.user_data["viewer"]][6]+'\n7. '+users_female[context.user_data["viewer"]][7]+'\n8. '+users_female[context.user_data["viewer"]][8]+'\n9. '+users_female[context.user_data["viewer"]][9]+'\n10. '+users_female[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        else:
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"][1]]+'\n3. '+users_male[context.user_data["viewer"][3]]+'\n4. '+users_male[context.user_data["viewer"][4]]+'\n5. '+users_male[context.user_data["viewer"][5]]+'\n6. '+users_male[context.user_data["viewer"][6]]+'\n7. '+users_male[context.user_data["viewer"][7]]+'\n8. '+users_male[context.user_data["viewer"][8]]+'\n9. '+users_male[context.user_data["viewer"][9]]+'\n10. '+users_male[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"]][1]+'\n3. '+users_male[context.user_data["viewer"]][3]+'\n4. '+users_male[context.user_data["viewer"]][4]+'\n5. '+users_male[context.user_data["viewer"]][5]+'\n6. '+users_male[context.user_data["viewer"]][6]+'\n7. '+users_male[context.user_data["viewer"]][7]+'\n8. '+users_male[context.user_data["viewer"]][8]+'\n9. '+users_male[context.user_data["viewer"]][9]+'\n10. '+users_male[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        
        return SEARCHING

    elif update.message.text == 'Редактировать': #zdes' nachinaetsya
        reply_keyboard = [['Фото', 'Текст', 'Отмена']]
        update.message.reply_text('Нажмите на фото или напишите какое поле хотите изменить только цифру',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True) )

        return EDITING

def editing(update: Update, context: CallbackContext) -> int:
    context.user_data["editing"] = 1
    if update.message.text == 'Отмена':
        return bio(update,context)
    elif update.message.text == 'Фото':
        update.message.reply_text(
            'Отправьте ваше фото', reply_markup=ReplyKeyboardRemove()
        )
        return EDITING_PHOTO
    elif update.message.text == 'Текст':
        update.message.reply_text(
            'Напишите цифру где хотите изменить', reply_markup=ReplyKeyboardRemove()
        )
        EDITING_TEXT
    else:
        update.message.reply_text('Вы ввели неправильно повторите пожайлуста сначала')
        return bio(update, context)
    
def editing_photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    context.user_data["photofile"] = photo_file
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg') # zdes u tebya put' u menya file
    
    return bio(update, context)

def editing_text(update: Update, context: CallbackContext) -> int:
    print(type(update.message.text))
    print(update.message.text)
    if update.message.text == '2':
        reply_keyboard = [['Мужчина', 'Женщина']]
        update.message.reply_text(
            'Выберите ваш пол',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        return GENDER
    elif update.message.text == '3':
        update.message.reply_text(
            'Напишите ваше имя и фамилию',
            reply_markup=ReplyKeyboardRemove(),
        )

        return SURNAME
    
    elif update.message.text == '4':
        update.message.reply_text('Напишите ваш ру')
        return RU
    
    elif update.message.text == '5':
        update.message.reply_text('Напишите ваш рост')
        return HEIGHT
    
    elif update.message.text == '6':
        update.message.reply_text('Напишите ваш вес')
        return AGE
    
    elif update.message.text == '7':
        update.message.reply_text('Напишите кем вы работаете')
        return SPECIALITY
    
    elif update.message.text == '8':
        update.message.reply_text('Напишите ваш ежемесячный доход')
        return INCOME
    
    elif update.message.text == '9':
        update.message.reply_text('Напишите ваш ежемесячный доход')
        return INCOME
    
    elif update.message.text == '10':
        context.user_data["editing"] = 2
        update.message.reply_text('Опишите себя в пару предложений')
        return BIO
        
    else:
        update.message.reply_text('Вы ввели неправильно повторите пожайлуста сначала')
        return bio(update, context)
        
    


def searching(update: Update, context: CallbackContext) -> int:
    if update.message.text == 'Следующий':
        context.user_data["viewer"] = context.user_data["viewer"] + 1
        reply_keyboard = [['Назад', 'Like', 'Следующий']]

        if context.user_data["gender"] == 'Мужчина':
            if len(users_female) == context.user_data["viewer"]:
                context.user_data["viewer"] = 0
            elif context.user_data["viewer"] == -1:
                context.user_data["viewer"] = len(users_female)-1
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"][1]]+'\n3. '+users_female[context.user_data["viewer"][3]]+'\n4. '+users_female[context.user_data["viewer"][4]]+'\n5. '+users_female[context.user_data["viewer"][5]]+'\n6. '+users_female[context.user_data["viewer"][6]]+'\n7. '+users_female[context.user_data["viewer"][7]]+'\n8. '+users_female[context.user_data["viewer"][8]]+'\n9. '+users_female[context.user_data["viewer"][9]]+'\n10. '+users_female[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"]][1]+'\n3. '+users_female[context.user_data["viewer"]][3]+'\n4. '+users_female[context.user_data["viewer"]][4]+'\n5. '+users_female[context.user_data["viewer"]][5]+'\n6. '+users_female[context.user_data["viewer"]][6]+'\n7. '+users_female[context.user_data["viewer"]][7]+'\n8. '+users_female[context.user_data["viewer"]][8]+'\n9. '+users_female[context.user_data["viewer"]][9]+'\n10. '+users_female[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        else:
            if len(users_male) == context.user_data["viewer"]:
                context.user_data["viewer"] = 0
            elif context.user_data["viewer"] == -1:
                context.user_data["viewer"] = len(users_male)-1
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"][1]]+'\n3. '+users_male[context.user_data["viewer"][3]]+'\n4. '+users_male[context.user_data["viewer"][4]]+'\n5. '+users_male[context.user_data["viewer"][5]]+'\n6. '+users_male[context.user_data["viewer"][6]]+'\n7. '+users_male[context.user_data["viewer"][7]]+'\n8. '+users_male[context.user_data["viewer"][8]]+'\n9. '+users_male[context.user_data["viewer"][9]]+'\n10. '+users_male[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"]][1]+'\n3. '+users_male[context.user_data["viewer"]][3]+'\n4. '+users_male[context.user_data["viewer"]][4]+'\n5. '+users_male[context.user_data["viewer"]][5]+'\n6. '+users_male[context.user_data["viewer"]][6]+'\n7. '+users_male[context.user_data["viewer"]][7]+'\n8. '+users_male[context.user_data["viewer"]][8]+'\n9. '+users_male[context.user_data["viewer"]][9]+'\n10. '+users_male[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        return SEARCHING1
        
    elif update.message.text == 'Назад':
        context.user_data["viewer"] = context.user_data["viewer"] - 1
        reply_keyboard = [['Назад', 'Like', 'Следующий']]

        if context.user_data["gender"] == 'Мужчина':
            if len(users_female) == context.user_data["viewer"]:
                context.user_data["viewer"] = 0
            elif context.user_data["viewer"] == -1:
                context.user_data["viewer"] = len(users_female)-1
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"][1]]+'\n3. '+users_female[context.user_data["viewer"][3]]+'\n4. '+users_female[context.user_data["viewer"][4]]+'\n5. '+users_female[context.user_data["viewer"][5]]+'\n6. '+users_female[context.user_data["viewer"][6]]+'\n7. '+users_female[context.user_data["viewer"][7]]+'\n8. '+users_female[context.user_data["viewer"][8]]+'\n9. '+users_female[context.user_data["viewer"][9]]+'\n10. '+users_female[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"]][1]+'\n3. '+users_female[context.user_data["viewer"]][3]+'\n4. '+users_female[context.user_data["viewer"]][4]+'\n5. '+users_female[context.user_data["viewer"]][5]+'\n6. '+users_female[context.user_data["viewer"]][6]+'\n7. '+users_female[context.user_data["viewer"]][7]+'\n8. '+users_female[context.user_data["viewer"]][8]+'\n9. '+users_female[context.user_data["viewer"]][9]+'\n10. '+users_female[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        else:
            if len(users_male) == context.user_data["viewer"]:
                context.user_data["viewer"] = 0
            elif context.user_data["viewer"] == -1:
                context.user_data["viewer"] = len(users_male)-1
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"][1]]+'\n3. '+users_male[context.user_data["viewer"][3]]+'\n4. '+users_male[context.user_data["viewer"][4]]+'\n5. '+users_male[context.user_data["viewer"][5]]+'\n6. '+users_male[context.user_data["viewer"][6]]+'\n7. '+users_male[context.user_data["viewer"][7]]+'\n8. '+users_male[context.user_data["viewer"][8]]+'\n9. '+users_male[context.user_data["viewer"][9]]+'\n10. '+users_male[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"]][1]+'\n3. '+users_male[context.user_data["viewer"]][3]+'\n4. '+users_male[context.user_data["viewer"]][4]+'\n5. '+users_male[context.user_data["viewer"]][5]+'\n6. '+users_male[context.user_data["viewer"]][6]+'\n7. '+users_male[context.user_data["viewer"]][7]+'\n8. '+users_male[context.user_data["viewer"]][8]+'\n9. '+users_male[context.user_data["viewer"]][9]+'\n10. '+users_male[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        return SEARCHING1
        
    elif update.message.text == 'Редактировать профиль':

        reply_keyboard = [['Фото', 'Отмена']]
        update.message.reply_text('Нажмите на фото или напишите какое поле хотите изменить только цифру',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True) )

        return EDITING
    elif update.message.text == 'Like':
        if context.user_data["gender"] == 'Мужчина':
            update.message.reply_text('Вы лайкнули пользовятеля '+ users_female[context.user_data["viewer"]][4] + 'что там еще')
            print("likeddd", context.user_data["surname"], users_female[context.user_data["viewer"]][4])
            database.like(context.user_data["surname"], users_female[context.user_data["viewer"]][4])

            chat_id_towrite = int(database.send_liked_message_male(users_female[context.user_data["viewer"]][4])[0])
            updater.bot.send_message(text="Вас лайкнул %s можете его тоже лайкнуть" % (context.user_data["surname"]), chat_id=chat_id_towrite)
            reply_keyboard = [['Назад', 'Like', 'Следующий']]
            print("MESSAGE TO", chat_id_towrite)
            updater.bot.send_photo(chat_id=chat_id_towrite, photo=open(context.user_data["path_to_photo"], 'rb'), caption='\n2. '+context.user_data["surname"]+'\n3. '+context.user_data["age"]+'\n4. '+context.user_data["bio"]+'\n5. '+context.user_data["ru"]+'\n6. '+context.user_data["income"]+'\n7. '+context.user_data["surname"]+'\n8. '+context.user_data["surname"]+'\n9. '+context.user_data["surname"]+'\n10. '+context.user_data["surname"] )
        else:
            update.message.reply_text('Вы лайкнули пользовятеля '+ users_male[context.user_data["viewer"]][4] + 'что там еще')
            print("likeddd", context.user_data["surname"], users_male[context.user_data["viewer"]][4])
            database.like(context.user_data["surname"], users_male[context.user_data["viewer"]][4])

            print(database.send_liked_message_female("AAA"))
            print("user to write find chat id", users_male[context.user_data["viewer"]][4])
            #print(users_male[context.user_data["viewer"]][4])[0]])
            chat_id_towrite = int(database.send_liked_message_male(users_male[context.user_data["viewer"]][4])[0])
            print("chat id founded", chat_id_towrite)
            updater.bot.send_message(text="Вас лайкнул %s можете его тоже лайкнуть" % (context.user_data["surname"]), chat_id=chat_id_towrite)
            reply_keyboard = [['Назад', 'Like', 'Следующий']]
            print("MESSAGE TO", chat_id_towrite)
            updater.bot.send_photo(chat_id=chat_id_towrite, photo=open(context.user_data["path_to_photo"], 'rb'), caption='\n2. '+context.user_data["surname"]+'\n3. '+context.user_data["age"]+'\n4. '+context.user_data["bio"]+'\n5. '+context.user_data["ru"]+'\n6. '+context.user_data["income"]+'\n7. '+context.user_data["surname"]+'\n8. '+context.user_data["surname"]+'\n9. '+context.user_data["surname"]+'\n10. '+context.user_data["surname"] )

        # zdes' update.message.from_user likenul female[context.user_data["review"]][3]
        reply_keyboard = [['Назад', 'Like', 'Следующий']]

        if context.user_data["gender"] == 'Мужчина':
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"][1]]+'\n3. '+users_female[context.user_data["viewer"][3]]+'\n4. '+users_female[context.user_data["viewer"][4]]+'\n5. '+users_female[context.user_data["viewer"][5]]+'\n6. '+users_female[context.user_data["viewer"][6]]+'\n7. '+users_female[context.user_data["viewer"][7]]+'\n8. '+users_female[context.user_data["viewer"][8]]+'\n9. '+users_female[context.user_data["viewer"][9]]+'\n10. '+users_female[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"]][1]+'\n3. '+users_female[context.user_data["viewer"]][3]+'\n4. '+users_female[context.user_data["viewer"]][4]+'\n5. '+users_female[context.user_data["viewer"]][5]+'\n6. '+users_female[context.user_data["viewer"]][6]+'\n7. '+users_female[context.user_data["viewer"]][7]+'\n8. '+users_female[context.user_data["viewer"]][8]+'\n9. '+users_female[context.user_data["viewer"]][9]+'\n10. '+users_female[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        else:
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"][1]]+'\n3. '+users_male[context.user_data["viewer"][3]]+'\n4. '+users_male[context.user_data["viewer"][4]]+'\n5. '+users_male[context.user_data["viewer"][5]]+'\n6. '+users_male[context.user_data["viewer"][6]]+'\n7. '+users_male[context.user_data["viewer"][7]]+'\n8. '+users_male[context.user_data["viewer"][8]]+'\n9. '+users_male[context.user_data["viewer"][9]]+'\n10. '+users_male[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"]][1]+'\n3. '+users_male[context.user_data["viewer"]][3]+'\n4. '+users_male[context.user_data["viewer"]][4]+'\n5. '+users_male[context.user_data["viewer"]][5]+'\n6. '+users_male[context.user_data["viewer"]][6]+'\n7. '+users_male[context.user_data["viewer"]][7]+'\n8. '+users_male[context.user_data["viewer"]][8]+'\n9. '+users_male[context.user_data["viewer"]][9]+'\n10. '+users_male[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
        print("MATCH", database.match(context.user_data["surname"]))
        #update.message.reply_text('У вас взаимность с ' + database.match(context.user_data["surname"]) + 'можете написать этому аккаунту')
        return SEARCHING1
        
def searching1(update: Update, context: CallbackContext) -> int:
    if update.message.text == 'Следующий':
        context.user_data["viewer"] = context.user_data["viewer"] + 1
        reply_keyboard = [['Назад', 'Like', 'Следующий']]

        if context.user_data["gender"] == 'Мужчина':
            if len(users_female) == context.user_data["viewer"]:
                context.user_data["viewer"] = 0
            elif context.user_data["viewer"] == -1:
                context.user_data["viewer"] = len(users_female)-1
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"][1]]+'\n3. '+users_female[context.user_data["viewer"][3]]+'\n4. '+users_female[context.user_data["viewer"][4]]+'\n5. '+users_female[context.user_data["viewer"][5]]+'\n6. '+users_female[context.user_data["viewer"][6]]+'\n7. '+users_female[context.user_data["viewer"][7]]+'\n8. '+users_female[context.user_data["viewer"][8]]+'\n9. '+users_female[context.user_data["viewer"][9]]+'\n10. '+users_female[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"]][1]+'\n3. '+users_female[context.user_data["viewer"]][3]+'\n4. '+users_female[context.user_data["viewer"]][4]+'\n5. '+users_female[context.user_data["viewer"]][5]+'\n6. '+users_female[context.user_data["viewer"]][6]+'\n7. '+users_female[context.user_data["viewer"]][7]+'\n8. '+users_female[context.user_data["viewer"]][8]+'\n9. '+users_female[context.user_data["viewer"]][9]+'\n10. '+users_female[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        else:
            if len(users_male) == context.user_data["viewer"]:
                context.user_data["viewer"] = 0
            elif context.user_data["viewer"] == -1:
                context.user_data["viewer"] = len(users_male)-1
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"][1]]+'\n3. '+users_male[context.user_data["viewer"][3]]+'\n4. '+users_male[context.user_data["viewer"][4]]+'\n5. '+users_male[context.user_data["viewer"][5]]+'\n6. '+users_male[context.user_data["viewer"][6]]+'\n7. '+users_male[context.user_data["viewer"][7]]+'\n8. '+users_male[context.user_data["viewer"][8]]+'\n9. '+users_male[context.user_data["viewer"][9]]+'\n10. '+users_male[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"]][1]+'\n3. '+users_male[context.user_data["viewer"]][3]+'\n4. '+users_male[context.user_data["viewer"]][4]+'\n5. '+users_male[context.user_data["viewer"]][5]+'\n6. '+users_male[context.user_data["viewer"]][6]+'\n7. '+users_male[context.user_data["viewer"]][7]+'\n8. '+users_male[context.user_data["viewer"]][8]+'\n9. '+users_male[context.user_data["viewer"]][9]+'\n10. '+users_male[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        return SEARCHING
        
    elif update.message.text == 'Назад':
        context.user_data["viewer"] = context.user_data["viewer"] - 1
        reply_keyboard = [['Назад', 'Like', 'Следующий']]

        if context.user_data["gender"] == 'Мужчина':
            if len(users_female) == context.user_data["viewer"]:
                context.user_data["viewer"] = 0
            elif context.user_data["viewer"] == -1:
                context.user_data["viewer"] = len(users_female)-1
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"][1]]+'\n3. '+users_female[context.user_data["viewer"][3]]+'\n4. '+users_female[context.user_data["viewer"][4]]+'\n5. '+users_female[context.user_data["viewer"][5]]+'\n6. '+users_female[context.user_data["viewer"][6]]+'\n7. '+users_female[context.user_data["viewer"][7]]+'\n8. '+users_female[context.user_data["viewer"][8]]+'\n9. '+users_female[context.user_data["viewer"][9]]+'\n10. '+users_female[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"]][1]+'\n3. '+users_female[context.user_data["viewer"]][3]+'\n4. '+users_female[context.user_data["viewer"]][4]+'\n5. '+users_female[context.user_data["viewer"]][5]+'\n6. '+users_female[context.user_data["viewer"]][6]+'\n7. '+users_female[context.user_data["viewer"]][7]+'\n8. '+users_female[context.user_data["viewer"]][8]+'\n9. '+users_female[context.user_data["viewer"]][9]+'\n10. '+users_female[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        else:
            if len(users_male) == context.user_data["viewer"]:
                context.user_data["viewer"] = 0
            elif context.user_data["viewer"] == -1:
                context.user_data["viewer"] = len(users_male)-1
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"][1]]+'\n3. '+users_male[context.user_data["viewer"][3]]+'\n4. '+users_male[context.user_data["viewer"][4]]+'\n5. '+users_male[context.user_data["viewer"][5]]+'\n6. '+users_male[context.user_data["viewer"][6]]+'\n7. '+users_male[context.user_data["viewer"][7]]+'\n8. '+users_male[context.user_data["viewer"][8]]+'\n9. '+users_male[context.user_data["viewer"][9]]+'\n10. '+users_male[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"]][1]+'\n3. '+users_male[context.user_data["viewer"]][3]+'\n4. '+users_male[context.user_data["viewer"]][4]+'\n5. '+users_male[context.user_data["viewer"]][5]+'\n6. '+users_male[context.user_data["viewer"]][6]+'\n7. '+users_male[context.user_data["viewer"]][7]+'\n8. '+users_male[context.user_data["viewer"]][8]+'\n9. '+users_male[context.user_data["viewer"]][9]+'\n10. '+users_male[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        return SEARCHING
        
    elif update.message.text == 'Редактировать профиль':

        reply_keyboard = [['Фото', 'Отмена']]
        update.message.reply_text('Нажмите на фото или напишите какое поле хотите изменить только цифру',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True) )

        return EDITING
    elif update.message.text == 'Like':
        update.message.reply_text('Вы лайкнули пользовятеля '+ users_male[context.user_data["viewer"]][4] + 'что там еще')
        print("likeeed feeemaleee", context.user_data["surname"], users_male[context.user_data["viewer"]][4])
        database.like(context.user_data["surname"], users_female[context.user_data["viewer"]][4])
        chat_id_towrite = int(database.send_liked_message_female(users_female[context.user_data["viewer"]][4])[0])
        updater.bot.send_message(text="Вас лайкнул %s можете его тоже лайкнуть" % (context.user_data["surname"]), chat_id=chat_id_towrite)
        reply_keyboard = [['Назад', 'Like', 'Следующий']]

        print("MESSAGE TO", chat_id_towrite)
        updater.bot.send_photo(chat_id=chat_id_towrite, photo=open(context.user_data["path_to_photo"], 'rb'), caption='\n2. '+context.user_data["surname"]+'\n3. '+context.user_data["age"]+'\n4. '+context.user_data["bio"]+'\n5. '+context.user_data["ru"]+'\n6. '+context.user_data["income"]+'\n7. '+context.user_data["surname"]+'\n8. '+context.user_data["surname"]+'\n9. '+context.user_data["surname"]+'\n10. '+context.user_data["surname"] )

        if context.user_data["gender"] == 'Мужчина':
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"][1]]+'\n3. '+users_female[context.user_data["viewer"][3]]+'\n4. '+users_female[context.user_data["viewer"][4]]+'\n5. '+users_female[context.user_data["viewer"][5]]+'\n6. '+users_female[context.user_data["viewer"][6]]+'\n7. '+users_female[context.user_data["viewer"][7]]+'\n8. '+users_female[context.user_data["viewer"][8]]+'\n9. '+users_female[context.user_data["viewer"][9]]+'\n10. '+users_female[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_female[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_female[context.user_data["viewer"]][1]+'\n3. '+users_female[context.user_data["viewer"]][3]+'\n4. '+users_female[context.user_data["viewer"]][4]+'\n5. '+users_female[context.user_data["viewer"]][5]+'\n6. '+users_female[context.user_data["viewer"]][6]+'\n7. '+users_female[context.user_data["viewer"]][7]+'\n8. '+users_female[context.user_data["viewer"]][8]+'\n9. '+users_female[context.user_data["viewer"]][9]+'\n10. '+users_female[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        else:
            #updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"][2]], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"][1]]+'\n3. '+users_male[context.user_data["viewer"][3]]+'\n4. '+users_male[context.user_data["viewer"][4]]+'\n5. '+users_male[context.user_data["viewer"][5]]+'\n6. '+users_male[context.user_data["viewer"][6]]+'\n7. '+users_male[context.user_data["viewer"][7]]+'\n8. '+users_male[context.user_data["viewer"][8]]+'\n9. '+users_male[context.user_data["viewer"][9]]+'\n10. '+users_male[context.user_data["viewer"][10]],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
            updater.bot.send_photo(chat_id=update.message.chat_id, photo=open(users_male[context.user_data["viewer"]][2], 'rb'), caption='\n2. '+users_male[context.user_data["viewer"]][1]+'\n3. '+users_male[context.user_data["viewer"]][3]+'\n4. '+users_male[context.user_data["viewer"]][4]+'\n5. '+users_male[context.user_data["viewer"]][5]+'\n6. '+users_male[context.user_data["viewer"]][6]+'\n7. '+users_male[context.user_data["viewer"]][7]+'\n8. '+users_male[context.user_data["viewer"]][8]+'\n9. '+users_male[context.user_data["viewer"]][9]+'\n10. '+users_male[context.user_data["viewer"]][10],reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )
        #print("MATCH", database.match(context.user_data["surname"][1]))
        #if database.match(context.user_data["surname"][1]) > 0:
            #print("Пара ")
            #update.message.reply_text('У вас взаимность с '+ database.match(context.user_data["surname"][1]) + 'можете написать этому аккаунту')
        return SEARCHING




def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    users.remove(str(update.message.chat_id))
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
            EDITING: [MessageHandler(Filters.text & ~Filters.command, editing)],
            EDITING_TEXT: [MessageHandler(Filters.text & ~Filters.command, editing_text)],
            EDITING_PHOTO: [MessageHandler(Filters.photo, editing_photo)],
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
