from fastapi import FastAPI
from app.database import engine, Base
from app.routers import products, orders
app = FastAPI(title='Склад')


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(products.router)
app.include_router(orders.router)