from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, BaseDB
from .routers import auth, photo, purchase, wallet
from .dependencies import get_current_user

app = FastAPI()

# Mengaktifkan CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BaseDB.metadata.create_all(bind=engine)

app.include_router(auth.auth_router)
app.include_router(photo.photo_router)
app.include_router(wallet.wallet_router)
app.include_router(purchase.purchase_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
