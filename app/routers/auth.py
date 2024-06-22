from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime
from ..models import User, TokenTable
from ..schemas import *
from decimal import Decimal
from ..database import get_db
from ..dependencies import *

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register/")
async def register(request: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_hashed_password(request.password)
    db_user = db.query(User).filter(User.username == request.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=request.username, password=hashed_password, fullname=request.fullname, contact=request.contact)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response_data=""
    return ResponseBase(message="User registered successfully", data=response_data, error=False)


@auth_router.post('/login')
def login(request: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = TokenTable(user_id=user.id, access_token=access, refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    response_data = TokenResponseData(access_token=access, refresh_token=refresh, id_user=user.id)
    return ResponseBase(message="Success login", data=response_data, error=False)

@auth_router.get('/getusers')
def getusers(session: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    users = session.query(User).all()
    response_data = [UserListResponseData(id=user.id, username=user.username, create_at=user.create_at, update_at=user.update_at) for user in users]
    return ResponseBase(message="Users retrieved successfully", data=response_data, error=False)

@auth_router.post('/change-password')
def change_password(request: changepassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()
    
    return ResponseBase(message="Password changed successfully", data=None, error=False)

@auth_router.post('/logout')
def logout(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload['sub']
    token_record = db.query(TokenTable).all()
    info = []
    for record in token_record:
        if (datetime.utcnow() - record.created_date).days > 1:
            info.append(record.user_id)
    if info:
        db.query(TokenTable).filter(TokenTable.user_id.in_(info)).delete()
        db.commit()
        
    existing_token = db.query(TokenTable).filter(TokenTable.user_id == user_id, TokenTable.access_token == token).first()
    if existing_token:
        existing_token.status = False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return ResponseBase(message="Logout Successfully", data=None, error=False)
