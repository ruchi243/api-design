import sqlite3 

DATABASE = "flight_bookings.db"

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

    cursor.execute("""
CREATE TABLE IF NOT EXISTS customers ( 
                   customer_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   customer_name TEXT NOT NULL, 
                   customer_email TEXT NOT NULL
                   )
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
                   flight_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   flight_name TEXT NOT NULL, 
                   origin TEXT NOT NULL, 
                   destination TEXT NOT NULL, 
                   date TEXT NOT NULL, 
                   time TEXT NOT NULL, 
                   capacity INTEGER NOT NULL, 
                   availability INTEGER NOT NULL
                   )
                   """)
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
                   reservation_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   customer_id INTEGER NOT NULL, 
                   flight_id INTEGER NOT NULL,
                   booked_at TEXT DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (customer_id) REFERENCES customers(customer_id), 
                   FOREIGN KEY(flight_id) REFERENCES flights(flight_id)
                   )
            
""")
    conn.commit()
    conn.close()