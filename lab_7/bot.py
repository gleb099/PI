import requests
from time import sleep  
from bs4 import BeautifulSoup
import datetime
import telebot
from telebot import types
import csv
import json
from pathlib import Path
import codecs

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

class BotHandler:

    # URL1 = "file:///C:/Users/%D0%93%D0%BB%D0%B5%D0%B1/Desktop/%D0%A3%D0%BD%D0%B8%D0%B2%D0%B5%D1%80/4%20%D0%BA%D1%83%D1%80%D1%81/%D0%9F%D0%B5%D1%80%D0%B5%D1%81%D0%B4%D0%B0%D1%87%D0%B8_%D0%9B%D0%B5%D1%82%D0%BE/%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D0%B0%D1%8F%20%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%B8%D1%8F/Turov_2.0/www.bontour.rutourstours-to-europePAGEN_1=1.html"
    URL = "https://www.bontour.ru/tours/tours-to-europe/?PAGEN_1=1"
    URL2 = "view-source:https://www.bontour.ru/tours/tours-to-europe/?PAGEN_1=1"
    URL1 = "www.bontour.rutourstours-to-europePAGEN_1=1.txt"
    URL1 = open(URL1, 'r')
    operData = []
    left_menu = []
    def get_html(self, url, params = None): #получаем доступ к сайту()потом и код пбудем получать
        # with open('www.bontour.rutourstours-to-europePAGEN_1=1.json') as users_file:
        #     users = json.load(users_file)
        r = requests.get(url, params)
        return r

    def get_content(self, html): #парсер основной инфы
        with codecs.open('www.bontour.rutourstours-to-europePAGEN_1=1.txt', 'r', 'utf_8_sig') as markup:
            soup = BeautifulSoup(markup.read())
        # soup = BeautifulSoup(html, 'html.parser')
        print(soup)
        items = soup.find_all('tr') #ищем на сайте тег tr
        print(items)

        self.operData = []        
        
        for item in items: #в теге tr ищем что-то
            item_tdid3 = item.find('td', class_ = 'tdid3')
            item_tdid4 = item.find('td', class_ = 'tdid4')
            item_tdid5 = item.find('td', class_ = 'tdid5')

            if item_tdid3 != None: #в td были ноны поэтому проифал
                self.operData.append({ #добавляю все данные в виде словарей в массив
                    'tour_name': item_tdid3.get_text(), #гет текст выдает только текст
                    'tour_waybill': item_tdid4.get_text(),
                    'tour_price': item_tdid5.get_text()
                })

        for i in range(len(self.operData)):
            print(self.operData[i], '\n')
        
        return self.operData

    def get_left_menu(self, html): #парсер левой части страницы(направления туров)
        with codecs.open('www.bontour.rutourstours-to-europePAGEN_1=1.txt', 'r', 'utf_8_sig') as markup:
            soup = BeautifulSoup(markup.read())
        # soup = BeautifulSoup(html, 'html.parser')
        items2 = soup.find_all('div', class_= 'leftmenu')
        self.left_menu = []

        for item2 in items2:
            item_li = item2.find_all('a')

            for item22 in item_li:
                self.left_menu.append({
                    'catalog_item': item22.get_text(),
                    'catalog_href': item22.get('href') #выдают саму ссылку из а-href
                    })

        for i in range(len(self.left_menu)):
            print(self.left_menu[i], '\n')

        return self.left_menu

    def parse(self):
        # html = self.get_html(self.URL)
        html = self.URL1
        # print(html.status_code) #если 200 код то все норм, если 404 или что-то в этом роде то нет
        # if html.status_code == 200: #тут гет запросы обычные, поэтому почти всегда будет 200
        #     print('Good connection') #но на всякий случай надо прочекать все
        # else:
        #     print('Error')

        print(self.get_content(html))
        return self.get_content(html)

    def parse_leftmenu(self):
        # html = self.get_html(self.URL)
        html = self.URL1
        # print(html.status_code)
        return self.get_left_menu(html)


    #Dima_shifr






#Работа с ботом

#https://api.telegram.org/bot1147491662:AAFzTza9v0chQM3WYLTjRdTGbJcELWY6Gds/getUpdates

# greetings = ('здравствуй', 'привет', 'ку', 'здорово')  
# now = datetime.datetime.now()

token = "1235071063:AAH5U4mIQPh3C_OwYaNSMuzT5TIexfwNg-o"
bot = telebot.TeleBot(token)
parser_tours = BotHandler()
parser_tours1 = BotHandler()
data_tours = parser_tours1.parse().copy() #выведи эту инфу просто и все
data_menu = parser_tours1.parse_leftmenu().copy()

print(data_tours)

print('TESTING')

global clientData
clientData = dict()

# print(data_menu)

@bot.message_handler(commands=['start'])
def start_message(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/start', '/stop')
    user_markup.row('Каталог наших туров')
    user_markup.row('Все туры')
    user_markup.row('Перейти на наш сайт')
    user_markup.row('Курс валют')
    user_markup.row('Контакты', 'Забронировать')
    bot.send_message(message.from_user.id, f'Приветствую, {message.from_user.first_name}! \nМеня зовут Туров! И я помогу тебе в выборе твоего идеального путешествия!', reply_markup=user_markup)

@bot.message_handler(commands=['stop'])
def start_message(message):
    hide_markup = telebot.types.ReplyKeyboardMarkup()
    bot.send_message(message.from_user.id, f'До скорой встречи, {message.from_user.first_name}', reply_markup=hide_markup)

@bot.message_handler(content_types = ['text'])
def get_text_messages(message):
    if message.text == 'Все туры':
        for i in range(len(data_tours)):
            bot.send_message(message.from_user.id, data_tours[i]['tour_name'] + 2 * '\n' + 'Цена: ' + data_tours[i]['tour_price'])
    elif message.text.lower() == 'каталог' or message.text == 'Каталог наших туров':
        for i in range(len(data_menu)):
            bot.send_message(message.from_user.id, data_menu[i]['catalog_item'])
    elif message.text.lower() == 'сайт' or message.text == 'Перейти на наш сайт':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Буду рад увидеть тебя на нашем сайте", url="https://www.bontour.ru/tours/europe/")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "Нажимай на кнопку БонТур.", reply_markup=keyboard)
    elif message.text.lower() == 'курс валют' or message.text == 'Курс валют':
        bot.send_message(message.chat.id, "Евро - 88.77 руб. Доллар - 73.00 руб.")
    elif message.text == 'Контакты':
        bot.send_message(message.chat.id, "ОФИС В МОСКВЕ +7 (495) 640-62-24 \n САНКТ-ПЕТЕРБУРГ +7 (812) 335-99-90")
    elif message.text.lower() == 'оставить заявку' or message.text == 'Забронировать':
        msg = bot.send_message(message.chat.id, f'{message.from_user.first_name} {message.from_user.last_name}, оставь свой номер телефона и с тобой скоро созвонится наш оператор!')
        bot.register_next_step_handler(msg, phone_num)

def phone_num(message):
    global number
    number = message.text
    print("Номер ", number)
    msg = bot.send_message(message.chat.id, f'{message.from_user.first_name}, напиши еще тур, который тебе больше всего интересен.')
    bot.register_next_step_handler(msg, tour_num)

def tour_num(message):
    global tour
    tour = message.text
    print(tour)
    msg = bot.send_message(message.chat.id, f'Введи серию и номер своего паспорта')
    bot.register_next_step_handler(msg, pas_num)

def pas_num(message):
    global pas
    pas = message.text
    print(pas)
    msg = bot.send_message(message.chat.id, f'Отлично, давай подтвердим данные?')
    bot.register_next_step_handler(msg, final)

def final(message):
    bot.send_message(message.chat.id, f'Тебя зовут {message.from_user.first_name} {message.from_user.last_name} \n Твой телефон {number} \n Выбранный тур {tour} \n Паспорт {pas} \n \n Данные отправлены! Жди звонка от менеджера для окончательного подтверждения и оплаты.' )
    key = f'{message.from_user.first_name} {message.from_user.last_name}'
    
    # tempData = clientData[f'{message.from_user.first_name} {message.from_user.last_name}'].copy()

    path = Path('users.json')
    clientData = json.loads(path.read_text(encoding='utf-8'))
    print(clientData)
    clientData[f'{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username}'] = []
    clientData[f'{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username}'].append(shifr(number, 4, 0))
    clientData[f'{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username}'].append(shifr(tour, 4, 0))
    clientData[f'{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username}'].append(shifr(pas, 4, 0))
    path.write_text(json.dumps(clientData), encoding='utf-8')
    print(clientData)

    # with open('users.json', 'w') as f:
    #     # json.dumps(clientData, f)
    #     f.write(json.dumps(clientData))

bot.polling(none_stop = True, interval = 0)


