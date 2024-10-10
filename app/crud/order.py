from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Order, OrderItem
from datetime import datetime
from app.schemas import OrderCreate, OrderItem


def create_order(db: AsyncSession, order: OrderCreate):
    db_order = Order(created_at=datetime.utcnow(), status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        create_order_item(db, db_order.id, item)

    return db_order


def get_orders(db: AsyncSession, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()


def get_order(db: AsyncSession, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def update_order_status(db: AsyncSession, order_id: int, status: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = status
        db.commit()
        db.refresh(order)
        return order
    return None


def create_order_item(db: AsyncSession, order_id: int, item: OrderItem):
    db_order_item = OrderItem(order_id=order_id, product_id=item.product_id, quantity=item.quantity)
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item


def update_order_item(db: AsyncSession, order_item_id: int, item: OrderItem):
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if order_item:
        order_item.product_id = item.product_id
        order_item.quantity = item.quantity
        db.commit()
        db.refresh(order_item)
        return order_item
    return None