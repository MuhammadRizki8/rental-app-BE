from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.responses import FileResponse
import os

from ..models import *
from ..schemas import *
from ..database import get_db
from ..dependencies import *

photo_router = APIRouter(prefix="/photos", tags=["photos"])

@photo_router.get("/", dependencies=[Depends(JWTBearer())])
async def read_all_photos(db: Session = Depends(get_db)):
    photos = db.query(Photo).all()
    response_data = [PhotoDetailResponseData(id_photo=photo.id_photo, id_author=photo.id_author, title=photo.title, description=photo.description, price=photo.price, path=photo.path,create_at=photo.create_at, update_at=photo.update_at) for photo in photos]
    return ResponseBase(message="Photos retrieved successfully", data=response_data, error=False)

@photo_router.post("/", dependencies=[Depends(JWTBearer())])
async def create_photo(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_photo = db.query(Photo).filter(Photo.title == title).first()
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

    db_photo = Photo(
        title=title,
        description=description,
        price=price,
        id_author=current_user.id,
        create_at=datetime.now(),
        update_at=datetime.now(),
        path=file.filename
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    
    response_data ={
            "id": db_photo.id_photo,
            "title": db_photo.title,
            "path": db_photo.path
        }
    return ResponseBase(message="Photos retrieved successfully", data=response_data, error=False)

@photo_router.get("/{photo_id}", dependencies=[Depends(JWTBearer())])
async def read_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = db.query(Photo).filter(Photo.id_photo == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    response_data = PhotoDetailResponseData(id_photo=db_photo.id_photo, id_author=db_photo.id_author, title=db_photo.title, description=db_photo.description, price=db_photo.price, path=db_photo.path,create_at=db_photo.create_at, update_at=db_photo.update_at)
    return ResponseBase(message="Photos retrieved successfully", data=response_data, error=False)

@photo_router.put("/{photo_id}", dependencies=[Depends(JWTBearer())])
async def update_photo(photo_id: int, photo: PhotoUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_photo = db.query(Photo).filter(Photo.id_photo == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    if db_photo.id_author != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this photo")
    for var, value in vars(photo).items():
        setattr(db_photo, var, value)
    db_photo.update_at = datetime.now()
    db.commit()
    db.refresh(db_photo)
    response_data = PhotoDetailResponseData(id_photo=db_photo.id_photo, id_author=db_photo.id_author, title=db_photo.title, description=db_photo.description, price=db_photo.price, path=db_photo.path,create_at=db_photo.create_at, update_at=db_photo.update_at)
    return ResponseBase(message="Photos updated successfully", data=response_data, error=False)

@photo_router.delete("/{photo_id}", dependencies=[Depends(JWTBearer())])
async def delete_photo(photo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_photo = db.query(Photo).filter(Photo.id_photo == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    if db_photo.id_author != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this photo")
    db.delete(db_photo)
    db.commit()

    return ResponseBase(message="Photos deleted successfully", data=None, error=False)

@photo_router.get("/getimage/{nama_file}", dependencies=[Depends(JWTBearer())])
async def get_image(nama_file: str):
    path = f"./data_file/{nama_file}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)
