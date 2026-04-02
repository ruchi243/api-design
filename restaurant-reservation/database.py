import sqlite3 

DATABASE = "restaurant.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS customers ( \
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL
                   )""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS tables (
                   table_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   capacity INTEGER NOT NULL 
                   )
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
                   reservation_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   table_id INTEGER NOT NULL, 
                   customer_id INTEGER NOT NULL, 
                   date TEXT NOT NULL, 
                   start_time TEXT NOT NULL, 
                   end_time TEXT NOT NULL, 
                   FOREIGN KEY (table_id) REFERENCES tables(table_id)
                   FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                   )
                   """)
    
    conn.commit()
    conn.close()