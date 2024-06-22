from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Order
from app.schemas import OrderCreate, OrderUpdate, OrderResponseData, ResponseBase
from app.database import get_db
from typing import List
orders_router = APIRouter(prefix="/orders", tags=["orders"])

@orders_router.post("/", response_model=OrderResponseData)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@orders_router.get("/{order_id}", response_model=OrderResponseData)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@orders_router.put("/{order_id}", response_model=OrderResponseData)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.dict().items():
        if value is not None:
            setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

@orders_router.delete("/{order_id}", response_model=ResponseBase)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return ResponseBase(message="Order deleted successfully", data=None, error=False)

@orders_router.get("/user/{user_id}", response_model=List[OrderResponseData])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    db_orders = db.query(Order).filter(Order.user_id == user_id).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return db_orders

@orders_router.patch("/{order_id}/status", response_model=OrderResponseData)
def update_order_status(order_id: int, status_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.status_id = status_id
    db.commit()
    db.refresh(db_order)
    return db_order