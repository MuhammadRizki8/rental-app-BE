from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import *
from database import engine
from auth import auth_router
from photo import photo_router
from wallet import wallet_router
from purchase import purchase_router
from dependencies import get_current_user

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

app.include_router(auth_router)
app.include_router(photo_router, dependencies=[Depends(get_current_user)])
app.include_router(wallet_router, dependencies=[Depends(get_current_user)])
app.include_router(purchase_router, dependencies=[Depends(get_current_user)])

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
