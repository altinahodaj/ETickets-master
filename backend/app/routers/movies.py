from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional

from app.db.session import get_db
from app.db import models
from app.schemas.movies import MovieCreate, MovieResponse, MovieListResponse

router = APIRouter(prefix="/api/cinemas/{cinema_id}/movies", tags=["movies"])
public_router = APIRouter(prefix="/api/movies", tags=["public-movies"], include_in_schema=False)


# ------------------------------
# Helpers
# ------------------------------
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


def photo_to_dict(p: models.Photo):
    return {
        "id": p.id,
        "imgClientPath": p.img_client_path,
        "imgPath": p.img_path,
        "name": p.name,
        "photoType": p.photo_type,
    }


def actor_to_dict(a: models.Actor):
    return {
        "id": a.id,
        "firstName": a.first_name,
        "lastName": a.last_name,
        "imgPath": a.img_path,
        "nationality": a.nationality,
        "genre": a.genre,
        "birth": a.birth.isoformat() if a.birth else None,
        "deleted": a.deleted,
        "photos": [
            {"id": p.id, "imgClientPath": p.img_client_path} for p in (a.photos or [])
        ],
    }


def movie_to_payload(m: models.Movie):
    # kjo është pjesa kyçe: kthejmë dict (jo ORM), që actors të jenë dict
    return {
        "id": m.id,
        "cinemaId": m.cinema_id,
        "title": m.title,
        "description": m.description,
        "genre": m.genre,
        "language": m.language,
        "lengthMinutes": m.length_minutes,
        "releaseYear": m.release_year,
        "director": m.director,
        "deleted": m.deleted,
        "avgRating": float(getattr(m, "avg_rating", 0.0) or 0.0),
        "totalReviews": int(getattr(m, "total_reviews", 0) or 0),
        "photos": [photo_to_dict(p) for p in (m.photos or [])],
        "actors": [actor_to_dict(a) for a in (m.actors or [])],
    }


# ------------------------------
# LIST MOVIES (by cinema)
# ------------------------------
@router.get("", response_model=dict)
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
        .options(
            joinedload(models.Movie.photos),
            joinedload(models.Movie.actors).joinedload(models.Actor.photos),
        )
        .filter(models.Movie.cinema_id == cinema_id, models.Movie.deleted == False)
        .all()
    )

    attach_review_stats(db, movies)

    # ✅ kthejmë payload dict për secilin movie, që mos ketë crash nga Pydantic
    result = []
    for m in movies:
        payload = movie_to_payload(m)
        result.append(MovieResponse.model_validate(payload).model_dump(by_alias=True))

    return {"result": result, "errors": [], "messages": []}


# ------------------------------
# GET SINGLE MOVIE (by cinema)
# ------------------------------
@router.get("/{movie_id}", response_model=dict)
def get_movie(movie_id: int, cinema_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Movie).options(
        joinedload(models.Movie.photos),
        joinedload(models.Movie.actors).joinedload(models.Actor.photos),
    )

    if cinema_id:
        query = query.filter(models.Movie.cinema_id == cinema_id)

    movie = query.filter(models.Movie.id == movie_id, models.Movie.deleted == False).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    attach_review_stats(db, [movie])

    payload = movie_to_payload(movie)
    movie_data = MovieResponse.model_validate(payload).model_dump(by_alias=True)

    return {"result": movie_data, "errors": [], "messages": []}


# ------------------------------
# GET SINGLE MOVIE (public)
# ------------------------------
@public_router.get("/{movie_id}", response_model=dict)
def get_public_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .options(
            joinedload(models.Movie.photos),
            joinedload(models.Movie.actors).joinedload(models.Actor.photos),
        )
        .filter(models.Movie.id == movie_id, models.Movie.deleted == False)
        .first()
    )
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    attach_review_stats(db, [movie])

    payload = movie_to_payload(movie)
    movie_data = MovieResponse.model_validate(payload).model_dump(by_alias=True)

    return {"result": movie_data, "errors": [], "messages": []}


# ------------------------------
# CREATE MOVIE
# ------------------------------
@router.post("", response_model=dict)
def create_movie(cinema_id: int, payload: MovieCreate, db: Session = Depends(get_db)):
    cinema = (
        db.query(models.Cinema)
        .filter(models.Cinema.id == cinema_id, models.Cinema.deleted == False)
        .first()
    )
    if not cinema:
        raise HTTPException(status_code=404, detail="Cinema not found")

    movie = models.Movie(
        cinema_id=cinema_id,
        title=payload.title,
        description=payload.description,
        genre=payload.genre,
        language=payload.language,
        length_minutes=payload.length_minutes,
        release_year=payload.release_year,
        director=payload.director,
        deleted=False,
    )
    db.add(movie)
    db.commit()
    db.refresh(movie)

    # review stats default
    setattr(movie, "avg_rating", 0.0)
    setattr(movie, "total_reviews", 0)

    data = MovieResponse.model_validate(movie_to_payload(movie)).model_dump(by_alias=True)
    return {"result": data, "errors": [], "messages": ["Movie created"]}


# ------------------------------
# UPDATE MOVIE
# ------------------------------
@router.put("/{movie_id}", response_model=dict)
def update_movie(cinema_id: int, movie_id: int, payload: MovieCreate, db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .filter(models.Movie.id == movie_id, models.Movie.cinema_id == cinema_id)
        .first()
    )
    if not movie or movie.deleted:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie.title = payload.title
    movie.description = payload.description
    movie.genre = payload.genre
    movie.language = payload.language
    movie.length_minutes = payload.length_minutes
    movie.release_year = payload.release_year
    movie.director = payload.director

    db.commit()
    db.refresh(movie)

    # ngarko lidhjet
    movie = (
        db.query(models.Movie)
        .options(
            joinedload(models.Movie.photos),
            joinedload(models.Movie.actors).joinedload(models.Actor.photos),
        )
        .filter(models.Movie.id == movie_id, models.Movie.deleted == False)
        .first()
    )

    attach_review_stats(db, [movie])

    data = MovieResponse.model_validate(movie_to_payload(movie)).model_dump(by_alias=True)
    return {"result": data, "errors": [], "messages": ["Movie updated"]}


# ------------------------------
# DELETE MOVIE (soft delete)
# ------------------------------
@router.delete("/{movie_id}", response_model=dict)
def delete_movie(cinema_id: int, movie_id: int, db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .filter(models.Movie.id == movie_id, models.Movie.cinema_id == cinema_id)
        .first()
    )
    if not movie or movie.deleted:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie.deleted = True
    db.commit()
    return {"result": True, "errors": [], "messages": ["Movie deleted (soft)"]}
