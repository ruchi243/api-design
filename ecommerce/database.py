"""
browse products, 
place orders
view order history

customers - customer_id, customer_name
products - product_id, product_name, total_availability, price
orders - order_id, customer_id, product_id, date, price_of_order 

get /api/products (query the availability)

post /orders create an order 

get /orders/{customer_id}

"""

import sqlite3 

DATABASE = "ecommerce.db"

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
CREATE TABLE IF NOT EXISTS customers 
                   (
                   customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   customer_name TEXT NOT NULL 
                   )
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS products 
                   (
                   product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   product_name TEXT NOT NULL ,
                   total_availability INTEGER NOT NULL,
                   price INTEGER NOT NULL  
                    
                   )
                   """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS orders 
                   (
                   order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   customer_id INTEGER NOT NULL,
                   product_id INTEGER NOT NULL ,
                   date TEXT NOT NULL,
                   FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                   FOREIGN KEY (product_id) REFERENCES products(product_id)
                   )
                   """)
    conn.commit()
    conn.close()