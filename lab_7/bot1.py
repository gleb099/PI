import requests
from time import sleep  
from bs4 import BeautifulSoup
import datetime
import telebot
from telebot import types
import csv
import json

def shifr(mes:str, key:int, menu:int):
    def chose(letter:str, key):
        alphabet_eng = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
        alphabet_ENG = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alphabet_rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        alphabet_RUS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        alphabet_num = "0123456789012345678901234567890123456789"

        if letter in alphabet_eng:
            position = alphabet_eng.find(letter)
            newPosition = position + key
            return alphabet_eng[newPosition]

        elif letter in alphabet_ENG:
            position = alphabet_ENG.find(letter)
            newPosition = position + key
            return alphabet_ENG[newPosition]

        elif letter in alphabet_rus:
            position = alphabet_rus.find(letter)
            newPosition = position + key
            return alphabet_rus[newPosition]

        elif letter in alphabet_RUS:
            position = alphabet_RUS.find(letter)
            newPosition = position + key
            return alphabet_RUS[newPosition]

        elif letter in alphabet_num:
            position = alphabet_num.find(letter)
            newPosition = position + key
            return alphabet_num[newPosition]
        else:
            return str(letter)
    #key: Зашифровать - 0, Расшифровать - 1
    mes2 = ""
    if menu == 0:
        for i in mes:
            mes2 += chose(i, key)
        return mes2
    elif menu == 1:
        for i in mes:
            mes2 += chose(i, -key)
        return mes2
    else:
        print("")

token = "999490022:AAFLTlXMd0hHnTZJD4PulTdQy1EOrir79Nk"
bot = telebot.TeleBot(token)

# data_menu = ['Gleb Shevchenko', 89855574067, 'Тур ВА-8', 'Паспорт 3645 234589']

@bot.message_handler(commands=['start'])
def start_message(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Войти')
    bot.send_message(message.from_user.id, f'B2B BOTS', reply_markup=user_markup)

@bot.message_handler(content_types = ['text'])
def get_text_messages(message):
    if message.text == 'Войти':
        msg = bot.send_message(message.from_user.id, f'Введи логин')
        bot.register_next_step_handler(msg, login)
    elif message.text == 'База клиентов':
    	with open('users.json') as users_file:
    		users = json.load(users_file)
    	print(users)
    	fio = list(users.keys())
    	info = list(users.values())
    	for i in range(len(info)):
            temp = info[i][-1]
            temp1 = info[i][-2]
            temp2 = info[i][-3]
            info[i][-1] = shifr(temp, 4, 1)
            info[i][-2] = shifr(temp1, 4, 1)
            info[i][-3] = shifr(temp2, 4, 1)

    	for i in range(len(fio)):
       		bot.send_message(message.from_user.id, f'{fio[i]} {info[i]}')

def login(message):
	global login
	print(login)
	login = message.text
	msg = bot.send_message(message.chat.id, f'Логин подтвержден. Введи пароль.')
	bot.register_next_step_handler(msg, passw)

def passw(message):
	global pas
	global users
	pas = message.text
	print(pas)
	msg = bot.send_message(message.chat.id, f'Доступ разрешен')
	with open('users.json') as users_file:
		users = json.load(users_file)
	bot.register_next_step_handler(msg, data)

def data(message):
	user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
	user_markup.row('/start', '/stop')
	user_markup.row('База клиентов')
	bot.send_message(message.from_user.id, f'Добро пожаловать', reply_markup=user_markup)

bot.polling(none_stop = True, interval = 0)