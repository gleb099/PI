#https://api.telegram.org/bot1235071063:AAH5U4mIQPh3C_OwYaNSMuzT5TIexfwNg-o/getUpdates

import datetime
import requests
import csv
import json
from pathlib import Path

#Cоздаем класс для гет запроса на json чат-бота

class Connect:
    token = '1235071063:AAH5U4mIQPh3C_OwYaNSMuzT5TIexfwNg-o'
    url = ''

    #конструктор класса
    def __init__(self,token):
        self.token = token
        self.url = f'https://api.telegram.org/bot1235071063:AAH5U4mIQPh3C_OwYaNSMuzT5TIexfwNg-o'

    #функция, в которой подключаемся к json бота
    def get_Updates(self, offset=None, timeout=30):
        method = '/getUpdates'
        params = dict(offset = offset, timeout = timeout)
        resp = requests.get(self.url + method, params)
        result_json = resp.json()['result']
        return result_json

    #получаем последние обновления из json бота
    def get_last_update(self):
        get_result = self.get_Updates()
        if len(get_result) == 0:
            last_update = []
        else:
            last_update = get_result[0]
        return last_update

#создаем объект класса
bot = Connect('1235071063:AAH5U4mIQPh3C_OwYaNSMuzT5TIexfwNg-o')

#основная функция работы чат-бота для Unit теста
def main():
    global now
    now = datetime.datetime.now()
    new_offset = None
    while True:
        last_update = bot.get_last_update()
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        path = Path('usersUnit.json') #получаем доступ к json
        clientData = json.loads(path.read_text(encoding='utf-8')) #открываем на прочтение и записываем наш словарь те данные, которые там уже были
        
        #обновление, шифрование и запись новых данных  
        clientData[f'Last chat text {now}'] = []
        
        clientData[f'Last chat text {now}'].append(last_chat_text)
        path.write_text(json.dumps(clientData), encoding='utf-8') #загружаем дамп базы в файл

        new_offset = last_update_id + 1

#вызов основной функции
main()