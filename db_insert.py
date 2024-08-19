import sqlite3

# Connect DB or create if not exist
conn = sqlite3.connect('lexington.db')

# Create Cursor
cursor = conn.cursor()

# Odczytywanie danych
cursor.execute('SELECT * FROM product_other_versions')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Zamknięcie połączenia
conn.close()