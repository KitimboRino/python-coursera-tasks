import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

# Reset the Counts table
cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

# Prompt for file name
fname = input('Enter file name: ')
if len(fname) < 1: 
    fname = 'mbox.txt'  # Use the larger dataset
fh = open(fname)

# Process the file
for line in fh:
    if not line.startswith('From: '): 
        continue
    pieces = line.split()
    email = pieces[1]
    # Extract the domain (organization)
    domain = email.split('@')[1]
    
    # Update or insert into the database
    cur.execute('SELECT count FROM Counts WHERE org = ?', (domain,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (domain,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (domain,))

# Commit changes
conn.commit()

# Retrieve and display the top organization
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

print("Top organizations by count:")
for row in cur.execute(sqlstr):
    print(f"{row[0]}: {row[1]}")

# Close the database connection
cur.close()
