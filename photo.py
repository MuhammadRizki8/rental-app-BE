from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas
from database import SessionLocal
from auth import get_current_user
from typing import List

photo_router = APIRouter(prefix="/photos", tags=["photos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@photo_router.get("/", response_model=List[schemas.Photo])
async def read_all_photos(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    photos = db.query(models.Photo).all()
    return photos

@photo_router.post("/", response_model=dict)
async def create_photo(photo: schemas.PhotoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing_photo = db.query(models.Photo).filter(models.Photo.title == photo.title).first()
    if existing_photo:
        raise HTTPException(status_code=400, detail="Photo with this title already exists")
    db_photo = models.Photo(**photo.dict(), id_author=current_user.id, create_at=datetime.now(), update_at=datetime.now())
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    response_data = {
        "message": "Photo created successfully",
        "data": {
            "id": db_photo.id_photo,
            "title": db_photo.title
            # Include other fields if needed
        },
        "error": False
    }
    return response_data

@photo_router.get("/{photo_id}", response_model=dict)
async def read_photo(photo_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_photo = db.query(models.Photo).filter(models.Photo.id_photo == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return db_photo

@photo_router.put("/{photo_id}", response_model=dict)
async def update_photo(photo_id: int, photo: schemas.PhotoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_photo = db.query(models.Photo).filter(models.Photo.id_photo == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    if db_photo.id_author != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this photo")
    for var, value in vars(photo).items():
        setattr(db_photo, var, value)  # Update the attributes with the new values
    db_photo.update_at = datetime.now()
    db.commit()
    db.refresh(db_photo)
    response_data = {
        "message": "Photo updated successfully",
        "data": db_photo,
        "error": False
    }
    return response_data

@photo_router.delete("/{photo_id}", response_model=dict)
async def delete_photo(photo_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_photo = db.query(models.Photo).filter(models.Photo.id_photo == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    if db_photo.id_author != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this photo")
    db.delete(db_photo)
    db.commit()
    response_data = {
        "message": "Photo deleted successfully",
        "data": db_photo,
        "error": False
    }
    return response_data
