import sqlite3

# Connect DB or create if not exist
conn = sqlite3.connect('lexington.db')

# Create Cursor
cursor = conn.cursor()

# Create Table
creat_table = '''
    CREATE TABLE lexington 
    (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    stock TEXT NOT NULL,
    sku TEXT NOT NULL,
    dims TEXT NOT NULL
    )
'''
#cursor.execute(creat_table)

# Adding Data
insert_commend = '''
    INSERT INTO lexington (id, name, stock, sku, dims)
    VALUES (?, ?, ?, ?, ?)
'''
#cursor.execute(insert_commend,('1','antilles','Will be available 08-22-24', '566-144C', '80W x 87D x 64H in.'))

# Make changes
#conn.commit()

# Odczytywanie danych
cursor.execute('SELECT * FROM lexington')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Zamknięcie połączenia
conn.close()