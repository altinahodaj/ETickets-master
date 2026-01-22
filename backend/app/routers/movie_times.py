from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.db import models

router = APIRouter(
    prefix="/api/cinemas/{cinema_id}/movies/{movie_id}/movie-times",
    tags=["movie_times"]
)

@router.get("")
def list_movie_times(cinema_id: int, movie_id: int, db: Session = Depends(get_db)):
    cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()
    if not cinema or cinema.deleted:
        raise HTTPException(status_code=404, detail="Cinema not found")

    movie = (
        db.query(models.Movie)
        .filter(models.Movie.id == movie_id, models.Movie.cinema_id == cinema_id)
        .first()
    )
    if not movie or movie.deleted:
        raise HTTPException(status_code=404, detail="Movie not found")

    times = (
        db.query(models.MovieTime)
        .filter(
            models.MovieTime.cinema_id == cinema_id,
            models.MovieTime.movie_id == movie_id,
            models.MovieTime.deleted == False
        )
        .all()
    )
    return {"result": times, "errors": [], "messages": []}

@router.post("")
def create_movie_time(cinema_id: int, movie_id: int, payload: dict, db: Session = Depends(get_db)):
    # Kontrollo cinema
    cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()
    if not cinema or cinema.deleted:
        raise HTTPException(status_code=404, detail="Cinema not found")

    # Kontrollo movie
    movie = (
        db.query(models.Movie)
        .filter(models.Movie.id == movie_id, models.Movie.cinema_id == cinema_id)
        .first()
    )
    if not movie or movie.deleted:
        raise HTTPException(status_code=404, detail="Movie not found")

    # hall_id duhet
    hall_id = payload.get("hall_id")
    if not hall_id:
        raise HTTPException(status_code=400, detail="hall_id is required")

    hall = (
        db.query(models.Hall)
        .filter(models.Hall.id == hall_id, models.Hall.cinema_id == cinema_id)
        .first()
    )
    if not hall or hall.deleted:
        raise HTTPException(status_code=404, detail="Hall not found")

    # datat duhet të jenë ISO string
    start_time = payload.get("start_time")
    end_time = payload.get("end_time")
    if not start_time or not end_time:
        raise HTTPException(status_code=400, detail="start_time and end_time are required")

    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid datetime format. Use ISO format like: 2026-01-14T20:00:00"
        )

    mt = models.MovieTime(
        cinema_id=cinema_id,
        hall_id=hall_id,
        movie_id=movie_id,
        start_time=start_dt,
        end_time=end_dt,
        deleted=False
    )
    db.add(mt)
    db.commit()
    db.refresh(mt)
    return {"result": mt, "errors": [], "messages": ["MovieTime created"]}

@router.delete("/{movie_time_id}")
def delete_movie_time(cinema_id: int, movie_id: int, movie_time_id: int, db: Session = Depends(get_db)):
    mt = (
        db.query(models.MovieTime)
        .filter(
            models.MovieTime.id == movie_time_id,
            models.MovieTime.cinema_id == cinema_id,
            models.MovieTime.movie_id == movie_id
        )
        .first()
    )
    if not mt:
        raise HTTPException(status_code=404, detail="MovieTime not found")

    mt.deleted = True
    db.commit()
    return {"result": True, "errors": [], "messages": ["MovieTime deleted (soft)"]}
