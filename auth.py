from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import models
from database import SessionLocal
from schemas import UserAuth

auth_router = APIRouter(prefix="/auth", tags=["auth"])

# Generate Secret Key using a secure method
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/register/", response_model=dict)
async def register(user: UserAuth, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "data": {"id": new_user.id, "username": new_user.username}, "error": False}

@auth_router.post("/login/", response_model=dict)
async def login(user: UserAuth, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)  # Token expires in 30 minutes
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"message": "Login successful", "data": {"access_token": access_token, "id": db_user.id, "username": db_user.username}, "error": False}

# Dependency untuk mendapatkan pengguna saat ini berdasarkan token
def get_current_user(token: str = Header(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        db_user = db.query(models.User).filter(models.User.username == username).first()
        if db_user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return db_user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

