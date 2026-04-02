from fastapi import FastAPI, Depends, HTTPException 
from database import get_db, init_db 
import sqlite3 
from schemas import CustomerResponse, CustomerCreate, ProductResponse, ProductCreate, OrderResponse, OrderCreate
from typing import List 
from datetime import datetime

app = FastAPI()
init_db()

"""

get /api/products (query the availability)

post /orders create an order 

get /orders/{customer_id}
"""

@app.get("/products", response_model = List[ProductResponse])

def get_products(db: sqlite3.Connection = Depends(get_db)):

    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM products"
    )

    products = cursor.fetchall()

    return [dict(p) for p in products]

@app.post("/orders", response_model = OrderResponse)

def create_order(order: OrderCreate, response_model = OrderResponse, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE customer_id = (?)", (order.customer_id,))

    customer = cursor.fetchone()
    if not customer:
        raise HTTPException(status_code = 404, detail = "Invalid Customer")
    
    cursor.execute("SELECT product_id FROM products WHERE product_id = (?)", (order.product_id,))

    product = cursor.fetchone()
    if not product:
        raise HTTPException(status_code = 404, detail = "Invalid Product")
    
    cursor.execute("SELECT availability FROM products WHERE product_id = (?)", (order.product_id,))
    a = cursor.fetchone()
    if a["availability"] == 0:
        raise HTTPException(status_code = 404, detail = "Product not found")
    
    cursor.execute("UPDATE products SET availability = availability -1 WHERE product_id = ?", (order.product_id,))

    cursor.execute("INSERT INTO orders (customer_id, product_id) VALUES (?, ?)",
                   (order.customer_id, order.product_id ))
    db.commit()
    order_id = cursor.lastrowid
    date = datetime.utcnow().isoformat()

    return {"order_id": order_id, "customer_id" : order.customer_id, "product_id" : order.product_id, "date" : date }


@app.get("/orders/{customer_id}", response_model = List[OrderResponse])

def get_orders(customer_id : int, db: sqlite3.Connection = Depends(get_db)):

    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM orders WHERE customer_id = (?)", (customer_id)
    )

    orders = cursor.fetchall()

    return [dict(o) for o in orders]

    

