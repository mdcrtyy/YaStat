import psycopg2

conn = psycopg2.connect(
    user="mdcrtyy",
    host="localhost",
    port="5432",
    database="yastat"
)

cur = conn.cursor()
cur.execute('''CREATE TABLE regions
(
    id varchar primary key,
    region_name varchar(64)
);

CREATE TABLE artists
(
    id INTEGER PRIMARY KEY,
    artist_name varchar(64) not null,
    artist_genre varchar(64) not null
);

CREATE TABLE regions_artists
(
    id serial primary key,
    fk_region_id varchar references regions,
    fk_artist_id integer references artists,
    region_listeners integer,
    date date,
    CHECK ( region_listeners >= 0 )
);

CREATE TABLE artists_data
(
    id serial primary key,
    fk_data_artist_id integer references artists,
    listeners integer,
    likes integer,
    date date,
    CHECK ( listeners >= 0 and likes >= 0)
);''')


cur.close()
conn.commit()
conn.close()

