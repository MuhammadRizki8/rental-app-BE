# routers/order_status.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import OrderStatus
from ..schemas import OrderStatusCreate, OrderStatusUpdate, OrderStatusResponseData, ResponseBase
from ..database import get_db

order_status_router = APIRouter(prefix="/order_status", tags=["order_status"])

@order_status_router.post("/", response_model=ResponseBase)
async def create_order_status(request: OrderStatusCreate, db: Session = Depends(get_db)):
    new_status = OrderStatus(status_name=request.status_name)
    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    response_data = OrderStatusResponseData(status_id=new_status.status_id, status_name=new_status.status_name)
    return ResponseBase(message="Order status created successfully", data=response_data.dict(), error=False)

@order_status_router.get("/{status_id}", response_model=ResponseBase)
async def get_order_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(OrderStatus).filter(OrderStatus.status_id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Order status not found")
    response_data = OrderStatusResponseData(status_id=status.status_id, status_name=status.status_name)
    return ResponseBase(message="Order status retrieved successfully", data=response_data.dict(), error=False)

@order_status_router.put("/{status_id}", response_model=ResponseBase)
async def update_order_status(status_id: int, request: OrderStatusUpdate, db: Session = Depends(get_db)):
    status = db.query(OrderStatus).filter(OrderStatus.status_id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Order status not found")
    if request.status_name:
        status.status_name = request.status_name
    db.commit()
    db.refresh(status)
    response_data = OrderStatusResponseData(status_id=status.status_id, status_name=status.status_name)
    return ResponseBase(message="Order status updated successfully", data=response_data.dict(), error=False)

@order_status_router.delete("/{status_id}", response_model=ResponseBase)
async def delete_order_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(OrderStatus).filter(OrderStatus.status_id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Order status not found")
    db.delete(status)
    db.commit()
    return ResponseBase(message="Order status deleted successfully", data=None, error=False)
