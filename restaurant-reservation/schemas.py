from pydantic import BaseModel 
from typing import Optional 

class CustomerCreate(BaseModel):
    customer_name : str 

class CustomerResponse(BaseModel):
    customer_id : int 
    customer_name : str 

class TableCreate(BaseModel): 
    capacity : int

class TableResponse(BaseModel):
    table_id : int 
    capacity : int 

class ReservationCreate(BaseModel):
    table_id : int 
    customer_id : int
    date : str 
    start_time : str 
    end_time : str 


class ReservationResponse(BaseModel):
    reservation_id : int 
    customer_id : int 
    table_id : int 
    date : str 
    start_time : str 
    end_time : str 
