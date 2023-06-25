import datetime
import requests
from bs4 import BeautifulSoup
import numpy as np

# Функция для парсинга и получения значений
def get_kp_reviews_data_week():
    # Проверяем, есть ли уже сохраненные значения для текущего дня
    today = datetime.date.today()
    filename = f"kp_week/reviews_week_kp_{today}.txt"
    try:
        with open(filename, 'r') as file:
            data = file.readlines()
        # Если есть сохраненные значения, возвращаем их
        return [int(value.strip()) for value in data]
    except FileNotFoundError:
        pass

    # Если нет сохраненных значений, выполняем парсинг
    url = "https://www.kinopoisk.ru/reviews/type/comment/period/week/#list"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Выполняем парсинг и получаем значения
    pos_value = int(soup.select_one('.resp_type li.pos b').text)
    neg_value = int(soup.select_one('.resp_type li.neg b').text)
    neut_value = int(soup.select_one('.resp_type li.neut b').text)

    # Сохраняем значения в файл
    with open(filename, 'w') as file:
        file.write(str(pos_value) + '\n')
        file.write(str(neg_value) + '\n')
        file.write(str(neut_value) + '\n')

    # Возвращаем полученные значения
    return [pos_value, neg_value, neut_value]
