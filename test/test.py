import psycopg2
import json

conn = psycopg2.connect(
    user="mdcrtyy",
    host="localhost",
    port="5432",
    database="yastat"
)


def insert_regions_data():
    with open('../data/input/info_about_regions.json', 'r') as f:
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
    with open('../data/input/all_genres.json', 'r') as f:
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


