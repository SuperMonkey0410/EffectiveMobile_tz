from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud.order import create_order, get_orders, get_order, update_order_status, update_order_item
from app.schemas import OrderCreate, OrderItem

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/orders/", response_model=OrderCreate)
def add_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db=db, order=order)


@router.get("/orders/", response_model=list[OrderCreate])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_orders(db=db, skip=skip, limit=limit)


@router.get("/orders/{id}", response_model=OrderCreate)
def read_order(id: int, db: Session = Depends(get_db)):
    order = get_order(db=db, order_id=id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/orders/{id}/status", response_model=OrderCreate)
def update_order_status_route(id: int, status: str, db: Session = Depends(get_db)):
    updated_order = update_order_status(db=db, order_id=id, status=status)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


@router.patch("/orders/{order_id}/items/{item_id}", response_model=OrderItem)
def update_order_item_route(order_id: int, item_id: int, item: OrderItem, db: Session = Depends(get_db)):
    updated_item = update_order_item(db=db, order_item_id=item_id, item=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Order item not found")
    return updated_item
