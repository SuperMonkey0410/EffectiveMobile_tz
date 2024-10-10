from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session  # Импортируем асинхронный генератор сессий
from app.crud.product import create_product, get_products, get_product, update_product, delete_product
from app.schemas import ProductCreate, Product

router = APIRouter()

@router.post("/products/", response_model=Product)
async def add_product(product: ProductCreate, db: AsyncSession = Depends(get_session)):
    return await create_product(db=db, product=product)  # используем await

@router.get("/products/", response_model=list[Product])
async def read_products(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    return await get_products(db=db, skip=skip, limit=limit)  # используем await

@router.get("/products/{id}", response_model=Product)
async def read_product(id: int, db: AsyncSession = Depends(get_session)):
    product = await get_product(db=db, product_id=id)  # используем await
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{id}", response_model=Product)
async def update_product_route(id: int, product: ProductCreate, db: AsyncSession = Depends(get_session)):
    updated_product = await update_product(db=db, product_id=id, product_data=product)  # используем await
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/products/{id}", response_model=Product)
async def delete_product_route(id: int, db: AsyncSession = Depends(get_session)):
    deleted_product = await delete_product(db=db, product_id=id)  # используем await
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product
