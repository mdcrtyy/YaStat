import psycopg2
import json


def insert_regions_data():
    conn = psycopg2.connect(
        user="mdcrtyy",
        host="localhost",
        port="5432",
        database="yastat"
    )

    with open('../../data/input/info_about_regions.json', 'r') as f:
        info_about_regions = json.load(f)

    regions = []
    for region_id, region_data in info_about_regions.items():
        region_name = region_data.get('name', '')
        population = region_data.get('population', '')
        regions.append((region_id, region_name, population))

    cur = conn.cursor()

    sql_regions = """INSERT INTO regions(id, region_name, population)
             VALUES (%s, %s, %s)"""

    cur.executemany(sql_regions, regions)
    conn.commit()
    cur.close()
    conn.close()


def insert_genres_data():
    conn = psycopg2.connect(
        user="mdcrtyy",
        host="localhost",
        port="5432",
        database="yastat"
    )

    with open('../../data/input/all_genres.json', 'r') as f:
        info_about_genres = json.load(f)

    genres = []
    for genre_id, genre_data in info_about_genres.items():
        genre_name = genre_data
        genres.append((genre_id, genre_name))

    cur = conn.cursor()

    sql_genres = """INSERT INTO genres(id, genre_name)
                 VALUES (%s, %s)"""

    cur.executemany(sql_genres, genres)
    conn.commit()
    cur.close()
    conn.close()


### Функция, заполняющая таблицу artists Айдишником и именем
def insert_artist_id_name(path):
    conn = psycopg2.connect(
        user="mdcrtyy",
        host="localhost",
        port="5432",
        database="yastat"
    )

    with open(f'{path}', 'r') as f:
        info_about_artist = json.load(f)

    artists = []
    for artist_id, artist_data in info_about_artist.items():
        artist_name = artist_data.get("Name", '')
        artists.append((artist_id, artist_name))

    cur = conn.cursor()

    sql_artists = """INSERT INTO artists(id, artist_name)
                     VALUES (%s, %s)
                     ON CONFLICT (id) DO NOTHING"""

    cur.executemany(sql_artists, artists)
    conn.commit()
    cur.close()
    conn.close()


# Функция, вставляющая количество слушателей, лайков и дату в таблицу artists_data
def insert_artist_data(path):
    conn = psycopg2.connect(
        user="mdcrtyy",
        host="localhost",
        port="5432",
        database="yastat"
    )

    with open(f'{path}', 'r') as f:
        info_about_artist = json.load(f)

    artists_count_of_list = []
    for artist_id, artist_data in info_about_artist.items():
        artist_listeners = artist_data.get("Listeners", '')
        artist_likes = artist_data.get("Likes", '')
        if type(artist_listeners) != int:
            artist_listeners = 0
        if type(artist_likes) != int:
            artist_likes = 0
        date = artist_data.get("date", '')
        artists_count_of_list.append((artist_id, artist_listeners, artist_likes, date))

    cur = conn.cursor()

    sql_artists_data = """INSERT INTO artists_data(fk_data_artist_id, listeners, likes, date)
                     VALUES (%s, %s, %s, %s)
                     """
    try:
        cur.executemany(sql_artists_data, artists_count_of_list)
    except psycopg2.errors.InvalidTextRepresentation as e:
        print("Error: ", e)

    conn.commit()
    cur.close()
    conn.close()
