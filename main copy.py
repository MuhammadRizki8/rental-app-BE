from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
from pydantic import BaseModel
import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

# Buat koneksi ke database menggunakan SQLAlchemy
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://your_username:your_password@localhost/gallery_app"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Definisikan model untuk tabel Pengguna (User)
class User(Base):
    __tablename__ = "User"
    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Model Pydantic untuk data pengguna yang akan diregistrasi
class UserRegistration(BaseModel):
    username: str
    password: str

# Model Pydantic untuk data login
class UserLogin(BaseModel):
    username: str
    password: str

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency untuk mendapatkan session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fungsi untuk verifikasi kata sandi
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Endpoint untuk proses login
@app.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint untuk proses registrasi pengguna
@app.post("/register/")
async def register_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    # Periksa apakah nama pengguna sudah ada dalam database
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash kata sandi sebelum menyimpannya
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())

    # Tambahkan pengguna ke database dengan kata sandi yang sudah di-hash
    new_user = User(username=user_data.username, password=hashed_password.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id_user}

# Secret key untuk pembuatan token
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Fungsi untuk membuat access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
