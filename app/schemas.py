from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    status: str

class OrderCreate(OrderBase):
    items: List[dict]  # Список элементов заказа

class Order(OrderBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True