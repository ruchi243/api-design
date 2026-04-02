from fastapi import FastAPI, Depends, HTTPException 
from database import get_db, init_db
import sqlite3 
from schemas import FlightResponse, FlightCreate, CustomerResponse, CustomerCreate, ReservationResponse, ReservationCreate 
from typing import List 

app = FastAPI()
init_db()

@app.post("/customers", response_model = CustomerResponse)

def create_customer(customer: CustomerCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO customers (customer_name, customer_email) VALUES (?,?)", 
        (customer.customer_name, customer.customer_email)
    )

    db.commit()
    customer_id = cursor.lastrowid
    return {"customer_id" : customer_id, "customer_name" : customer.customer_name, "customer_email" : customer.customer_email}

@app.get("/customers/{customer_id}", response_model = CustomerResponse)

def get_customer(customer_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers WHERE customer_id = (?)", (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        raise HTTPException(status_code = 404, detail = "Customer not found")
    
    return dict(customer)

@app.post("/flights", response_model = FlightResponse)

def create_flight(flight : FlightCreate, db : sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO flights (flight_name, origin, destination, date, time, capacity, availability) VALUES (?,?,?,?,?,?,?)", 
        (flight.flight_name, flight.origin, flight.destination, flight.date, flight.time, flight.capacity,flight.capacity)
        )
    db.commit()
    flight_id = cursor.lastrowid
    return {"flight_id" : flight_id, "flight_name" : flight.flight_name, "origin" : flight.origin, "destination" : flight.destination, "date" : flight.date, "time" : flight.time, "capacity" : flight.capacity, "availability" : flight.capacity}

@app.get("/flights/{flight_id}", response_model = FlightResponse)

def get_flight(flight_id : int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM flights WHERE flight_id = (?)", (flight_id, ))
    flight = cursor.fetchone()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return dict(flight)
    
from typing import Optional

@app.get("/flights", response_model=List[FlightResponse])
def get_all_available_flights(origin: Optional[str] = None, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    if origin:
        cursor.execute("SELECT * FROM flights WHERE availability > 0 AND origin = ?", (origin,))
    else:
        cursor.execute("SELECT * FROM flights WHERE availability > 0")
    flights = cursor.fetchall()
    if not flights:
        raise HTTPException(status_code=404, detail="No available flights")
    return [dict(row) for row in flights]
@app.get("/reservations/{reservation_id}", response_model = ReservationResponse)

def get_reservation(reservation_id, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reservations WHERE reservation_id = (?)", (reservation_id, ))
    reservation = cursor.fetchone()
    if not reservation:
        raise HTTPException(status_code = 404, detail = "Reservation not found")
    return dict(reservation)

@app.post("/reservations", response_model = ReservationResponse)

def create_reservation(reservation : ReservationCreate, db : sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers WHERE customer_id = (?)", (reservation.customer_id, ))
    customer = cursor.fetchone()
    if not customer:
        raise HTTPException(status_code = 404, detail = "Customer not found")
    
    cursor.execute("SELECT * FROM flights WHERE flight_id = (?)", (reservation.flight_id, ))
    flight = cursor.fetchone()
    if not flight:
        raise HTTPException(status_code = 404, detail = "Flight not found")
    
    cursor.execute("SELECT availability FROM flights WHERE flight_id = (?)", (reservation.flight_id,))
    availability = cursor.fetchone()
    if availability["availability"] == 0:
        raise HTTPException(status_code = 404, detail = "No available flights")
    cursor.execute(
    "UPDATE flights SET availability = availability - 1 WHERE flight_id = ?",
    (reservation.flight_id,))

    cursor.execute("INSERT INTO reservations (customer_id, flight_id) VALUES (?, ?)", (reservation.customer_id, reservation.flight_id))
    db.commit()
    reservation_id = cursor.lastrowid
    return {"reservation_id" : reservation_id, "customer_id" : reservation.customer_id, "flight_id" : reservation.flight_id, "booked_at" : ""}
