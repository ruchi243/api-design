from fastapi import FastAPI, Depends, HTTPException 
from database import get_db, init_db 
import sqlite3 
from schemas import CustomerResponse, CustomerCreate, TableResponse, TableCreate, ReservationResponse, ReservationCreate
from typing import List 

app = FastAPI()
init_db()

@app.post("/customers", response_model = CustomerResponse)

def create_customer(customer: CustomerCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO customers (customer_name) VALUES (?)", 
        (customer.customer_name,)
    )
    db.commit()
    customer_id = cursor.lastrowid 
    return {"customer_id" : customer_id, "customer_name": customer.customer_name}
@app.post("/tables", response_model = TableResponse)

def create_table(table: TableCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO tables (capacity) VALUES (?)", 
        (table.capacity,)
        
    )
    db.commit()
    table_id = cursor.lastrowid
    return {"table_id": table_id, "capacity": table.capacity}

@app.post("/reservations", response_model = ReservationResponse)


def create_reservation(reservation: ReservationCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (reservation.customer_id, ))
    customer = cursor.fetchone()
    if not customer:
        raise HTTPException(status_code = 404, detail = "Customer not found")
    cursor.execute("SELECT * FROM tables WHERE table_id = ?", (reservation.table_id, ))
    table = cursor.fetchone()
    if not table:
        raise HTTPException(status_code = 404, detail = "Table not found")
    
    cursor.execute(
    """SELECT * FROM reservations 
    WHERE table_id = ? 
    AND start_time < ? 
    AND end_time > ?""",
    (reservation.table_id, reservation.end_time, reservation.start_time)
)
    conflict = cursor.fetchone()
    if conflict:
        raise HTTPException(status_code = 409, detail = "Table already exists for this slot")
    
    cursor.execute(
        "INSERT INTO reservations (table_id, customer_id, date, start_time, end_time) VALUES (?, ?, ?, ?, ?)", 
        (reservation.table_id, reservation.customer_id, reservation.date, reservation.start_time, reservation.end_time, )
    )
    db.commit()
    reservation_id = cursor.lastrowid
    return {"reservation_id": reservation_id, "customer_id" : reservation.customer_id, "table_id": reservation.table_id, "date": reservation.date, "start_time": reservation.start_time, "end_time": reservation.end_time}


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return dict(customer)

@app.get("/tables/{table_id}", response_model = TableResponse)

def get_table(table_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tables WHERE table_id = ?", (table_id, ))
    table = cursor.fetchone()
    if not table:
        raise HTTPException(status_code=404, detail = "Table not found")
    return dict(table)

@app.get("/reservations/{reservation_id}", response_model = ReservationResponse)

def get_reservation(reservation_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reservations WHERE reservation_id = ?", (reservation_id, ))
    reservation = cursor.fetchone()
    if not reservation:
        raise HTTPException(status_code = 404, detail = "Reservation not found")
    return dict(reservation)
@app.get("/tables", response_model=List[TableResponse])
def get_tables(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tables")
    return [dict(row) for row in cursor.fetchall()]
@app.delete("/reservations/{reservation_id}")

def delete_reservation(reservation_id : int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reservations WHERE reservation_id = ?", (reservation_id, ))
    reservation = cursor.fetchone()
    if not reservation:
        raise HTTPException(status_code = 404, detail = "Reservation not found")
    cursor.execute("DELETE FROM reservations WHERE reservation_id = ?", (reservation_id, ))
    db.commit()
    return {"message": "Reservation deleted"}
