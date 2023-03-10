"""
Модуль, который содержит функцию, возвращающую словарь
вида {'id': {'Name': 'name, 'Genre': list_of_artist_genres}}
"""
import re
import requests
from bs4 import BeautifulSoup as bs


def get_id_name_genres_of_artist(url):
    data = {}
    try:
        request = requests.get(url)
        soup = bs(request.text, "html.parser")

        artist_content = soup.find_all('div', class_='artist__content')
        # Общий жанр (Главный жанр)
        main_genre = soup.find('h1', class_='d-header__title-text typo typo-h1_big').text
        for artist in artist_content:
            artist_name = artist.find('a', class_='d-link deco-link', href=True).text
            artist_id = int(
                re.findall(r'^/artist/\s*(.*)', str(artist.find('a', class_='d-link deco-link', href=True)['href']))[0])
            artist_genres = artist.find_all('a', class_='d-link deco-link d-link_muted deco-link_muted')
            list_of_genres = [main_genre.lower()]
            for genre in artist_genres:
                if genre.text != main_genre.lower():
                    list_of_genres.append(genre.text)
            data[artist_id] = {'Name': artist_name, 'Genres': list_of_genres}

    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    except bs.exceptions.BeautifulSoup as e:
        print(f'Failed to parse HTML: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')
    finally:
        return data

