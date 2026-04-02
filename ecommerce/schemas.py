from pydantic import BaseModel 
from typing import Optional


class CustomerCreate(BaseModel):
    customer_name : str 

class CustomerResponse(BaseModel):
    customer_id : int 
    customer_name : str 

class ProductCreate(BaseModel):
    product_name : str 
    total_availability : int
    price : int 

class ProductResponse(BaseModel):
    product_id : int
    product_name : str 
    total_availability : int
    price : int 

class OrderCreate(BaseModel):
    customer_id : int 
    product_id : int 

class OrderResponse(BaseModel):
    order_id : int 
    customer_id : int 
    product_id : int 
    date : str
