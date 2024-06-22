from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserUpdate, UserResponseData, ResponseBase
from app.database import get_db
import shutil
import os

users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.get("/{user_id}", response_model=UserResponseData)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@users_router.put("/{user_id}", response_model=UserResponseData)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.dict().items():
        if value is not None:
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@users_router.post("/{user_id}/upload-photo", response_model=ResponseBase)
def upload_photo(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    upload_dir = "uploads/profile_photos"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    db_user.photo_url = f"/uploads/profile_photos/{file.filename}"
    db.commit()
    db.refresh(db_user)
    
    return ResponseBase(message="Profile photo uploaded successfully", data=db_user.photo_url, error=False)

