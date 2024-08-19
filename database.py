import sqlite3
from sqlite3 import Connection

DATABASE_NAME = 'lexington.db'

def get_db_connection() -> Connection:
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON")  # Włączenie wsparcia dla kluczy obcych
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    '''Tworzenie tabeli Category'''
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

    '''Tworzenie tabeli Products'''
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sku TEXT NOT NULL,
                dimensions TEXT NOT NULL,
                stock status TXT NOT NULL
                
            )
        ''')

    '''Tworzenie tabeli Product Attribute'''
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS product_attribute (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             product_id INTEGER,
             attribute_key TEXT,
             attribute_value TEXT,
             FOREIGN KEY (product_id) REFERENCES products(id)
         )
     ''')

    '''Tworzenie tabeli Product Other Versions'''
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS product_other_versions (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             product_id INTEGER,
             name TEXT,
             sku TEXT,
             dimensions TEXT,
             FOREIGN KEY (product_id) REFERENCES products(id)
         )
     ''')

    conn.commit()
    conn.close()

def main():
    conn = get_db_connection()
    tables = create_tables()

if __name__ == "__main__":
    main()
