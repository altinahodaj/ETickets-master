from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models

router = APIRouter(prefix="/api", tags=["Reviews"])


# --------- Schemas (Pydantic) ---------

class ReviewCreate(BaseModel):
    review_title: str
    review_description: str
    review_rating: int
    user_id: str
    user_name: str


class ReviewOut(BaseModel):
    id: int
    movie_id: int
    review_title: str
    review_description: str
    review_rating: int
    user_id: str
    user_name: str
    insert_date: datetime
    deleted: bool

    class Config:
        from_attributes = True  # Pydantic v2


# --------- Routes ---------

@router.get("/movies/{movie_id}/reviews", response_model=list[ReviewOut])
def list_reviews(movie_id: int, db: Session = Depends(get_db)):
    # kontrollo a ekziston filmi (opsionale por e dobishme)
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    reviews = (
        db.query(models.Review)
        .filter(
            models.Review.movie_id == movie_id,
            models.Review.deleted == False,
        )
        .order_by(models.Review.insert_date.desc())
        .all()
    )
    return reviews


@router.post("/movies/{movie_id}/reviews", response_model=ReviewOut)
def create_review(movie_id: int, payload: ReviewCreate, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # (opsionale) validim i rating
    if payload.review_rating < 1 or payload.review_rating > 5:
        raise HTTPException(status_code=400, detail="review_rating must be between 1 and 5")

    review = models.Review(
        movie_id=movie_id,
        review_title=payload.review_title,
        review_description=payload.review_description,
        review_rating=payload.review_rating,
        user_id=payload.user_id,
        user_name=payload.user_name,
        insert_date=datetime.utcnow(),
        deleted=False,
    )

    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.delete("/reviews/{review_id}")
def soft_delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.deleted = True
    db.commit()
    return {"ok": True}
