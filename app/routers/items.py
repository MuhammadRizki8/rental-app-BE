from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.models import Item, Vendor
from app.schemas import ItemCreate, ItemUpdate, ItemResponseData, ResponseBase
from app.database import get_db
from datetime import datetime
import os
from fastapi.responses import FileResponse
from typing import List

items_router = APIRouter(prefix="/items", tags=["items"])

UPLOAD_DIRECTORY = "uploads"  # Directory to store uploaded images

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@items_router.post("/", response_model=ResponseBase)
async def create_item(
    item_name: str = Form(...),
    description: str = Form(...),
    price_per_day: float = Form(...),
    vendor_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    existing_item = db.query(Item).filter(Item.item_name == item_name).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Item with this name already exists")

    vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    # Upload file
    try:
        contents = await file.read()
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Error uploading file")
    finally:
        await file.close()

    image_url = f"{file.filename}"

    db_item = Item(
        item_name=item_name,
        description=description,
        price_per_day=price_per_day,
        image_url=image_url,
        created_at=datetime.now(),
        vendor_id=vendor_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    response_data = {
        "item_id": db_item.item_id,
        "item_name": db_item.item_name,
        "image_url": db_item.image_url,
        "vendor_id": db_item.vendor_id
    }
    return ResponseBase(message="Item created successfully", data=response_data, error=False)

@items_router.get("/{item_id}", response_model=ItemResponseData)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.item_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@items_router.put("/{item_id}", response_model=ItemResponseData)
async def update_item(
    item_id: int,
    item_name: str = Form(...),
    description: str = Form(...),
    price_per_day: float = Form(...),
    vendor_id: int = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_item = db.query(Item).filter(Item.item_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    if file:
        try:
            contents = await file.read()
            file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
            with open(file_location, 'wb') as f:
                f.write(contents)
            image_url = f"/uploads/{file.filename}"
            db_item.image_url = image_url
        except Exception:
            raise HTTPException(status_code=500, detail="Error uploading file")
        finally:
            await file.close()

    db_item.item_name = item_name
    db_item.description = description
    db_item.price_per_day = price_per_day
    db_item.vendor_id = vendor_id

    db.commit()
    db.refresh(db_item)
    return db_item

@items_router.delete("/{item_id}", response_model=ResponseBase)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.item_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return ResponseBase(message="Item deleted successfully", data=None, error=False)

@items_router.get("/getimage/{nama_file}")
async def get_image(nama_file: str):
    path = f"./uploads/{nama_file}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)

@items_router.get("/", response_model=List[ItemResponseData])
def get_all_items(search: str = None, db: Session = Depends(get_db)):
    if search:
        db_items = db.query(Item).filter(Item.item_name.contains(search)).all()
    else:
        db_items = db.query(Item).all()
    return db_items
