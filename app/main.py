from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, BaseDB
from .routers import auth, items, order_status, orders, vendors, ratings, users
from fastapi.staticfiles import StaticFiles
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
app.include_router(order_status.order_status_router)
app.include_router(items.items_router)
app.include_router(orders.orders_router)
app.include_router(vendors.vendors_router)
app.include_router(ratings.ratings_router)
app.include_router(users.users_router) 
# Serve static files from the uploads directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
