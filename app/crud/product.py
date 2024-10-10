from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.schemas import ProductCreate

def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: AsyncSession, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

def get_product(db: AsyncSession, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: AsyncSession, product_id: int, product_data: ProductCreate):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        for key, value in product_data.dict().items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product
    return None

def delete_product(db: AsyncSession, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return product
    return None