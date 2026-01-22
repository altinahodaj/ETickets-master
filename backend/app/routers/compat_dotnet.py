from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models

router = APIRouter(prefix="/api", tags=["compat_dotnet"])


# -----------------------------
# CINEMAS
# -----------------------------
@router.get("/cinemas/")
def dotnet_cinemas(db: Session = Depends(get_db)):
    cinemas = (
        db.query(models.Cinema)
        .filter(models.Cinema.deleted == False)
        .all()
    )
    return {"result": cinemas}


@router.get("/cinemas/{cinema_id}")
def dotnet_cinema(cinema_id: int, db: Session = Depends(get_db)):
    cinema = (
        db.query(models.Cinema)
        .filter(models.Cinema.id == cinema_id, models.Cinema.deleted == False)
        .first()
    )
    return {"result": cinema}


# -----------------------------
# MOVIES
# -----------------------------
@router.get("/movies/")
def dotnet_movies(db: Session = Depends(get_db)):
    movies = (
        db.query(models.Movie)
        .filter(models.Movie.deleted == False)
        .all()
    )
    return {"result": movies}


@router.get("/cinemas/{cinema_id}/movies")
def dotnet_cinema_movies(cinema_id: int, db: Session = Depends(get_db)):
    movies = (
        db.query(models.Movie)
        .filter(
            models.Movie.cinema_id == cinema_id,
            models.Movie.deleted == False,
        )
        .all()
    )
    return {"result": movies}


# -----------------------------
# EVENTS (showtimes = MovieTime)
# -----------------------------
@router.get("/events/")
def dotnet_events(db: Session = Depends(get_db)):
    events = (
        db.query(models.MovieTime)
        .filter(models.MovieTime.deleted == False)
        .all()
    )
    return {"result": events}


@router.get("/cinemas/{cinema_id}/events")
def dotnet_cinema_events(cinema_id: int, db: Session = Depends(get_db)):
    events = (
        db.query(models.MovieTime)
        .filter(
            models.MovieTime.cinema_id == cinema_id,
            models.MovieTime.deleted == False,
        )
        .all()
    )
    return {"result": events}


# -----------------------------
# ACTORS (placeholder for now)
# -----------------------------
@router.get("/actors/")
def dotnet_actors():
    return {"result": []}
