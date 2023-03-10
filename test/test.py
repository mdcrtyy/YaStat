"""
Модуль, вовзращающий словарь жанров в виде ключ-значение, где ключ - название на английском
"""

import re
import requests
from bs4 import BeautifulSoup as bs

headers = {'Accept-Language': 'en-US,en;q=1'}


def get_all_genres(url):
    data = {}
    request = requests.get(url, headers=headers)
    soup = bs(request.text, "html.parser")

    genres_block = soup.find('div', class_='page-main__metatags-line page-main__metatags-line_deep page-main__metatags-line_columns page-main__metatags-line_columns-c4')
    print(genres_block)
    return data


