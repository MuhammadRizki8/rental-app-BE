from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import models
import schemas
from database import SessionLocal
from dependencies import *
from fastapi.responses import FileResponse
import os

photo_router = APIRouter(prefix="/photos", tags=["photos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@photo_router.get("/", dependencies=[Depends(JWTBearer())])
async def read_all_photos(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    photos = db.query(models.Photo).all()
    response_data = {
        "message": "Photos retrieved successfully",
        "data": photos,
        "error": False
    }
    return response_data

@photo_router.post("/", response_model=dict, dependencies=[Depends(JWTBearer())])
async def create_photo(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    existing_photo = db.query(models.Photo).filter(models.Photo.title == title).first()
    if existing_photo:
        raise HTTPException(status_code=400, detail="Photo with this title already exists")

    # Upload file
    try:
        contents = await file.read()
        file_location = f"./data_file/{file.filename}"
        with open(file_location, 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Error uploading file")
    finally:
        await file.close()

    db_photo = models.Photo(
        title=title,
        description=description,
        price=price,
        id_author=current_user.id,
        create_at=datetime.now(),
        update_at=datetime.now(),
        file_path=file.filename
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    
    response_data = {
        "message": "Photo created successfully",
        "data": {
            "id": db_photo.id_photo,
            "title": db_photo.title,
            "file_path": db_photo.file_path
        },
        "error": False
    }
    return response_data

@photo_router.get("/{photo_id}", response_model=dict, dependencies=[Depends(JWTBearer())])
async def read_photo(photo_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_photo = db.query(models.Photo).filter(models.Photo.id_photo == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    response_data = {
        "message": "Photo retrieved successfully",
        "data": {"id_photo": db_photo.id_photo, "id_author": db_photo.id_author, "title": db_photo.title, "description": db_photo.description, "price": db_photo.price, "create_at": db_photo.create_at, "update_at": db_photo.update_at, "file_path": db_photo.file_path},
        "error": False
    }
    return response_data

@photo_router.put("/{photo_id}", response_model=dict, dependencies=[Depends(JWTBearer())])
async def update_photo(photo_id: int, photo: schemas.PhotoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_photo = db.query(models.Photo).filter(models.Photo.id_photo == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    if db_photo.id_author != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this photo")
    for var, value in vars(photo).items():
        setattr(db_photo, var, value)
    db_photo.update_at = datetime.now()
    db.commit()
    db.refresh(db_photo)
    response_data = {
        "message": "Photo updated successfully",
        "data": {"id_photo": db_photo.id_photo, "title": db_photo.title, "description": db_photo.description, "price": db_photo.price},
        "error": False
    }
    return response_data

@photo_router.delete("/{photo_id}", response_model=dict, dependencies=[Depends(JWTBearer())])
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
        "data": {"id_photo": db_photo.id_photo},
        "error": False
    }
    return response_data

@photo_router.get("/getimage/{nama_file}", response_model=dict, dependencies=[Depends(JWTBearer())])
async def get_image(nama_file: str):
    file_path = f"./data_file/{nama_file}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
