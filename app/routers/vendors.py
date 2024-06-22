# routers/vendors.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Vendor
from app.schemas import VendorCreate, VendorUpdate, VendorResponseData, ResponseBase
from app.database import get_db

vendors_router = APIRouter(prefix="/vendors", tags=["vendors"])

@vendors_router.post("/vendors/", response_model=VendorResponseData)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    db_vendor = Vendor(**vendor.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

@vendors_router.get("/vendors/{vendor_id}", response_model=VendorResponseData)
def read_vendor(vendor_id: int, db: Session = Depends(get_db)):
    db_vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@vendors_router.put("/vendors/{vendor_id}", response_model=VendorResponseData)
def update_vendor(vendor_id: int, vendor: VendorUpdate, db: Session = Depends(get_db)):
    db_vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    for key, value in vendor.dict().items():
        if value is not None:
            setattr(db_vendor, key, value)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

@vendors_router.delete("/vendors/{vendor_id}", response_model=ResponseBase)
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    db_vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    db.delete(db_vendor)
    db.commit()
    return ResponseBase(message="Vendor deleted successfully", data=None, error=False)
