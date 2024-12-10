import sqlite3
import json
import codecs

conn = sqlite3.connect('opengeo.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
fhand = codecs.open('where.js', 'w', "utf-8")
fhand.write("myData = [\n")
count = 0

for row in cur:
    try:
        data = str(row[1].decode() if isinstance(row[1], bytes) else row[1])
        js = json.loads(data)

        if len(js['features']) == 0:
            print(f"No features for: {row[0]}")
            continue

        lat = js['features'][0]['geometry']['coordinates'][1]
        lng = js['features'][0]['geometry']['coordinates'][0]
        where = js['features'][0]['properties']['display_name']
        where = where.replace("'", "")

        print(f"Processing: {where}")

        count = count + 1
        if count > 1:
            fhand.write(",\n")
        
        output = f"[{lat},{lng}, '{where}']"
        fhand.write(output)

    except Exception as e:
        print(f"Error processing row: {e}")
        print(f"Problematic data: {row}")
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")