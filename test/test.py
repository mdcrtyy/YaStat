"""
Модуль, вовзращающий словарь жанров в виде ключ-значение, где ключ - название на английском
"""

import re
import requests
from bs4 import BeautifulSoup as bs

headers = {'Accept-Language': 'en-US,en;q=1'}


def get_artist_name_id_genres(url):
    data = {}
    request = requests.get(url, headers=headers)
    soup = bs(request.text, "html.parser")

    artist_content = soup.find_all('div', class_='artist__content')
    # Общий жанр (Главный жанр)
    main_genre = soup.find('h1', class_='d-header__title-text typo typo-h1_big').text
    for artist in artist_content:
        artist_name = artist.find('a', class_='d-link deco-link', href=True).text
        artist_id = int(re.findall(r'^/artist/\s*(.*)', str(artist.find('a', class_='d-link deco-link', href=True)['href']))[0])
        artist_genres = artist.find_all('a', class_='d-link deco-link d-link_muted deco-link_muted')
        print('Name: ', artist_name)
        print('artist_id: ', artist_id)
        list_of_genres = [main_genre.lower()]
        for genre in artist_genres:
            if genre.text != 'рэп и хип-хоп':
                list_of_genres.append(genre.text)
        print('all_artist_genres: ', list_of_genres)
        data[artist_id] = {'Name': artist_name, 'Genres': list_of_genres}
    return data


