import sqlite3

# Connect to the SQLite database (or create a new one if it doesn't exist)
conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Create fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER PRIMARY KEY,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER PRIMARY KEY,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER PRIMARY KEY,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER PRIMARY KEY,
    title TEXT UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

# Open the CSV file
handle = open('tracks.csv')

# Example of CSV content:
# Name,Artist,Album,Genre,Count,Rating,Length
# Another One Bites The Dust,Queen,Greatest Hits,Rock,55,100,217103

for line in handle:
    line = line.strip()
    pieces = line.split(',')
    
    # Skip invalid lines
    if len(pieces) < 7:
        continue

    # Extract fields
    name = pieces[0]
    artist = pieces[1]
    album = pieces[2]
    genre = pieces[3]
    count = pieces[4]
    rating = pieces[5]
    length = pieces[6]

    print(name, artist, album, genre, count, rating, length)

    # Insert or ignore into Artist table
    cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
    cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
    artist_id = cur.fetchone()[0]

    # Insert or ignore into Genre table
    cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
    cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
    genre_id = cur.fetchone()[0]

    # Insert or ignore into Album table
    cur.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)', (album, artist_id))
    cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
    album_id = cur.fetchone()[0]

    # Insert or replace into Track table
    cur.execute('''
        INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count) 
        VALUES (?, ?, ?, ?, ?, ?)''',
        (name, album_id, genre_id, length, rating, count)
    )

# Commit changes and close the database connection
conn.commit()
conn.close()

print("Database creation complete.")
