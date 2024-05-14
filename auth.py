from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime
import models
import schemas
from decimal import Decimal
from database import get_db
from dependencies import *

auth_router = APIRouter(prefix="/auth", tags=["auth"])

# Fungsi untuk membuat wallet baru saat membuat user baru
def create_initial_wallet(db: Session, user_id: int):
    initial_balance = Decimal('30.00')  # Saldo awal 30
    new_wallet = models.Wallet(balance=initial_balance, id_user=user_id)
    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)
    return new_wallet

@auth_router.post("/register/", response_model=dict)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_hashed_password(user.password)
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = models.User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Membuat wallet baru untuk user yang terdaftar
    new_wallet=create_initial_wallet(db, new_user.id)

    return {"message": "User registered successfully", "data": {"id": new_user.id, "username": new_user.username, "id_wallet":new_wallet.id_wallet}, "error": False}

@auth_router.post('/login', response_model=dict)
def login(request: schemas.requestdetails, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = models.TokenTable(user_id=user.id, access_token=access, refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "message": "success login",
        "data": {"access_token": access, "refresh_token": refresh},
        "error": False
    }

@auth_router.get('/getusers')
def getusers(session: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    user = session.query(models.User).all()
    return user

@auth_router.post('/change-password')
def change_password(request: schemas.changepassword, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()
    
    return {"message": "Password changed successfully"}

@auth_router.post('/logout')
def logout(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload['sub']
    token_record = db.query(models.TokenTable).all()
    info = []
    for record in token_record:
        if (datetime.utcnow() - record.created_date).days > 1:
            info.append(record.user_id)
    if info:
        db.query(models.TokenTable).filter(models.TokenTable.user_id.in_(info)).delete()
        db.commit()
        
    existing_token = db.query(models.TokenTable).filter(models.TokenTable.user_id == user_id, models.TokenTable.access_token == token).first()
    if existing_token:
        existing_token.status = False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return {"message": "Logout Successfully"}
