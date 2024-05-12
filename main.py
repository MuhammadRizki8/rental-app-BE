from fastapi import FastAPI
import models
from database import engine
from auth import auth_router
from photo import photo_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(photo_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
