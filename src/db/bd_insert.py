import psycopg2
import json

conn = psycopg2.connect(
    user="mdcrtyy",
    host="localhost",
    port="5432",
    database="yastat"
)

with open('../../data/test.json', 'r') as f:
    existing_data = json.load(f)

with open('../../data/regions.json', 'r') as f:
    regions_list = json.load(f)

cur = conn.cursor()

# запрос для заполнения таблицы regions
for region_name in regions_list:
    cur.execute("INSERT INTO regions (id, region_name) VALUES (%s, %s);", (region_name, region_name))


# запрос для заполнения таблицы artists

artists = []
for artist_id, artist_data in existing_data.items():
    name = artist_data.get('Name', '')
    genre = artist_data.get('Genre', '')
    artists.append((artist_id, name, genre))

sql_artists = """INSERT INTO artists(id, artist_name, artist_genre)
         VALUES (%s, %s, %s)"""

cur.executemany(sql_artists, artists)

# запрос для заполнения таблицы artists_data
listeners_likes = []
for artist_id, artist_data in existing_data.items():
    date = artist_data.get('date', '')
    listeners = artist_data.get('Listeners', 0)
    likes = artist_data.get('Likes', 0)
    listeners_likes.append((artist_id, listeners, likes, date))

sql_artists_data = """INSERT INTO artists_data(fk_data_artist_id, listeners, likes, date)
         VALUES (%s, %s, %s, %s)"""

cur.executemany(sql_artists_data, listeners_likes)

# запрос для заполнения таблицы regions_artists
for artistid, artist_data in existing_data.items():
    artist_date = artist_data['date']
    for region_name, region_listeners in artist_data['Regions'].items():
        cur.execute(
            'INSERT INTO regions_artists (fk_region_id, fk_artist_id, region_listeners, date) VALUES (%s, %s, %s, %s)',
            (region_name, artistid, region_listeners, artist_date)
        )

conn.commit()
cur.close()
conn.close()
