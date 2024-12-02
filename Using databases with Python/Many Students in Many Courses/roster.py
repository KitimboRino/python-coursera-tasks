import json
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# Database setup: Create tables
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER PRIMARY KEY,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER PRIMARY KEY,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

# Prompt user for file name or use default
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'roster_data_sample.json'

# Load JSON data from file
with open(fname) as file:
    json_data = json.load(file)

# Insert data into tables
for entry in json_data:
    name = entry[0]
    title = entry[1]
    role = entry[2]  # Add role from JSON data

    print(f'Processing: Name={name}, Title={title}, Role={role}')

    # Insert into User table
    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES (?)''', (name,))
    cur.execute('SELECT id FROM User WHERE name = ?', (name,))
    user_id = cur.fetchone()[0]

    # Insert into Course table
    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES (?)''', (title,))
    cur.execute('SELECT id FROM Course WHERE title = ?', (title,))
    course_id = cur.fetchone()[0]

    # Insert into Member table
    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) 
        VALUES (?, ?, ?)''', (user_id, course_id, role))

# Commit changes to database
conn.commit()

# Verification query
print("\nVerifying data with query:")
query = '''
SELECT User.name, Course.title, Member.role
FROM User
JOIN Member ON User.id = Member.user_id
JOIN Course ON Course.id = Member.course_id
ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2;
'''
for row in cur.execute(query):
    print(row)

# Generate the required unique string
print("\nGenerating unique string:")
unique_query = '''
SELECT 'XYZZY' || hex(User.name || Course.title || Member.role) AS X
FROM User
JOIN Member ON User.id = Member.user_id
JOIN Course ON Course.id = Member.course_id
ORDER BY X LIMIT 1;
'''
for row in cur.execute(unique_query):
    print(row)

# Close the database connection
cur.close()
