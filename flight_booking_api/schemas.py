from pydantic import BaseModel 
from typing import Optional 

class CustomerCreate(BaseModel):
    customer_name : str 
    customer_email : str 

class CustomerResponse(BaseModel):
    customer_id : int 
    customer_name : str 
    customer_email : str 

class FlightCreate(BaseModel):
    flight_name : str 
    origin : str 
    destination : str 
    date : str 
    time : str 
    capacity : int 

class FlightResponse(BaseModel):
    flight_id : int
    flight_name : str 
    origin : str 
    destination : str 
    date : str 
    time : str 
    capacity : int
    availability : int 

class ReservationCreate(BaseModel):
    customer_id : int 
    flight_id : int 

class ReservationResponse(BaseModel):
    reservation_id : int 
    customer_id : int 
    flight_id : int
    booked_at : str

