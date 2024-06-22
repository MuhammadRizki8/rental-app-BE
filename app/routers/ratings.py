# routers/ratings.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Rating
from app.schemas import RatingCreate, RatingUpdate, RatingResponseData, ResponseBase
from app.database import get_db

ratings_router = APIRouter(prefix="/ratings", tags=["ratings"])

@ratings_router.post("/ratings/", response_model=RatingResponseData)
def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    db_rating = Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@ratings_router.get("/ratings/{rating_id}", response_model=RatingResponseData)
def read_rating(rating_id: int, db: Session = Depends(get_db)):
    db_rating = db.query(Rating).filter(Rating.rating_id == rating_id).first()
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating

@ratings_router.put("/ratings/{rating_id}", response_model=RatingResponseData)
def update_rating(rating_id: int, rating: RatingUpdate, db: Session = Depends(get_db)):
    db_rating = db.query(Rating).filter(Rating.rating_id == rating_id).first()
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    for key, value in rating.dict().items():
        if value is not None:
            setattr(db_rating, key, value)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@ratings_router.delete("/ratings/{rating_id}", response_model=ResponseBase)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    db_rating = db.query(Rating).filter(Rating.rating_id == rating_id).first()
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    db.delete(db_rating)
    db.commit()
    return ResponseBase(message="Rating deleted successfully", data=None, error=False)
