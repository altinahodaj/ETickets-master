from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.db.session import get_db
from app.db import models

router = APIRouter(prefix="/api/cinemas/{cinema_id}/movies", tags=["movies"])


def attach_review_stats(db: Session, movies: list[models.Movie]):
    if not movies:
        return

    movie_ids = [m.id for m in movies]

    rows = (
        db.query(
            models.Review.movie_id.label("movie_id"),
            func.avg(models.Review.review_rating).label("avg_rating"),
            func.count(models.Review.id).label("total_reviews"),
        )
        .filter(models.Review.movie_id.in_(movie_ids))
        .filter(models.Review.deleted == False)
        .group_by(models.Review.movie_id)
        .all()
    )

    rating_map = {
        r.movie_id: {
            "avg_rating": float(r.avg_rating) if r.avg_rating is not None else 0.0,
            "total_reviews": int(r.total_reviews) if r.total_reviews is not None else 0,
        }
        for r in rows
    }

    for m in movies:
        stats = rating_map.get(m.id, {"avg_rating": 0.0, "total_reviews": 0})
        setattr(m, "avg_rating", round(stats["avg_rating"], 1))
        setattr(m, "total_reviews", stats["total_reviews"])


@router.get("")
def list_movies(cinema_id: int, db: Session = Depends(get_db)):
    cinema = (
        db.query(models.Cinema)
        .filter(models.Cinema.id == cinema_id, models.Cinema.deleted == False)
        .first()
    )
    if not cinema:
        raise HTTPException(status_code=404, detail="Cinema not found")

    movies = (
        db.query(models.Movie)
        .options(joinedload(models.Movie.photos))
        .filter(models.Movie.cinema_id == cinema_id, models.Movie.deleted == False)
        .all()
    )

    attach_review_stats(db, movies)

    return {"result": movies, "errors": [], "messages": []}


@router.get("/{movie_id}")
def get_movie(cinema_id: int, movie_id: int, db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .options(joinedload(models.Movie.photos))
        .filter(
            models.Movie.id == movie_id,
            models.Movie.cinema_id == cinema_id,
            models.Movie.deleted == False,
        )
        .first()
    )
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    attach_review_stats(db, [movie])

    return {"result": movie, "errors": [], "messages": []}


@router.post("")
def create_movie(cinema_id: int, payload: dict, db: Session = Depends(get_db)):
    cinema = (
        db.query(models.Cinema)
        .filter(models.Cinema.id == cinema_id, models.Cinema.deleted == False)
        .first()
    )
    if not cinema:
        raise HTTPException(status_code=404, detail="Cinema not found")

    title = payload.get("title")
    if not title:
        raise HTTPException(status_code=400, detail="title is required")

    movie = models.Movie(
        cinema_id=cinema_id,
        title=title,
        description=payload.get("description"),
        genre=payload.get("genre"),
        language=payload.get("language"),
        length_minutes=payload.get("length_minutes"),
        release_year=payload.get("release_year"),
        director=payload.get("director"),
        deleted=False,
    )
    db.add(movie)
    db.commit()
    db.refresh(movie)

    setattr(movie, "avg_rating", 0.0)
    setattr(movie, "total_reviews", 0)

    return {"result": movie, "errors": [], "messages": ["Movie created"]}


@router.put("/{movie_id}")
def update_movie(cinema_id: int, movie_id: int, payload: dict, db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .filter(
            models.Movie.id == movie_id,
            models.Movie.cinema_id == cinema_id,
        )
        .first()
    )
    if not movie or movie.deleted:
        raise HTTPException(status_code=404, detail="Movie not found")

    for field in [
        "title",
        "description",
        "genre",
        "language",
        "length_minutes",
        "release_year",
        "director",
        "deleted",
    ]:
        if field in payload:
            setattr(movie, field, payload[field])

    db.commit()
    db.refresh(movie)

    attach_review_stats(db, [movie])

    return {"result": movie, "errors": [], "messages": ["Movie updated"]}


@router.delete("/{movie_id}")
def delete_movie(cinema_id: int, movie_id: int, db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .filter(
            models.Movie.id == movie_id,
            models.Movie.cinema_id == cinema_id,
        )
        .first()
    )
    if not movie or movie.deleted:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie.deleted = True
    db.commit()
    return {"result": True, "errors": [], "messages": ["Movie deleted (soft)"]}
