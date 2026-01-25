from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

from app.db.session import get_db
from app.db import models
from app.schemas.movie_times import MovieTimeCreate, MovieTimeResponse, MovieTimeListResponse

router = APIRouter(
    prefix="/api",
    tags=["movie_times"]
)

public_router = APIRouter(
    prefix="/api/MovieTimes",
    tags=["movie_times"],
    include_in_schema=False
)


@router.get("/cinemas/{cinema_id}/movies/{movie_id}/movie-times", response_model=MovieTimeListResponse)
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
        .options(joinedload(models.MovieTime.hall))
        .filter(
            models.MovieTime.cinema_id == cinema_id,
            models.MovieTime.movie_id == movie_id,
            models.MovieTime.deleted == False
        )
        .all()
    )
    return MovieTimeListResponse(result=times).model_dump(by_alias=True)


@public_router.get("", response_model=MovieTimeListResponse)
def list_public_movie_times(movie_id: int, db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .filter(models.Movie.id == movie_id, models.Movie.deleted == False)
        .first()
    )
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    times = (
        db.query(models.MovieTime)
        .options(joinedload(models.MovieTime.hall))
        .filter(
            models.MovieTime.movie_id == movie_id,
            models.MovieTime.deleted == False
        )
        .all()
    )
    return MovieTimeListResponse(result=times).model_dump(by_alias=True)

@router.get("/movies/{movie_id}/movie-times", response_model=MovieTimeListResponse, include_in_schema=False)
def list_movie_times_for_movie(movie_id: int, db: Session = Depends(get_db)):
    times = (
        db.query(models.MovieTime)
        .options(joinedload(models.MovieTime.hall))
        .filter(
            models.MovieTime.movie_id == movie_id,
            models.MovieTime.deleted == False
        )
        .all()
    )
    return MovieTimeListResponse(result=times).model_dump(by_alias=True)


@router.get("/MovieTimes/{id}", response_model=dict, include_in_schema=False)
@router.get("/movie-times/{id}", response_model=dict, include_in_schema=False)
def get_movie_time_generic(id: int, db: Session = Depends(get_db)):
    mt = (
        db.query(models.MovieTime)
        .options(joinedload(models.MovieTime.hall))
        .filter(models.MovieTime.id == id, models.MovieTime.deleted == False)
        .first()
    )
    if not mt:
        raise HTTPException(status_code=404, detail="Movie time not found")

    return {
        "result": MovieTimeResponse.model_validate(mt).model_dump(by_alias=True),
        "errors": [],
        "messages": []
    }


@router.get("/cinemas/{cinema_id}/movies/{movie_id}/movie-times/{id}", response_model=dict)
def get_movie_time(cinema_id: int, movie_id: int, id: int, db: Session = Depends(get_db)):
    mt = (
        db.query(models.MovieTime)
        .options(joinedload(models.MovieTime.hall))
        .filter(
            models.MovieTime.id == id,
            models.MovieTime.cinema_id == cinema_id,
            models.MovieTime.movie_id == movie_id,
            models.MovieTime.deleted == False
        )
        .first()
    )
    if not mt:
        raise HTTPException(status_code=404, detail="Movie time not found")

    return {
        "result": MovieTimeResponse.model_validate(mt).model_dump(by_alias=True),
        "errors": [],
        "messages": []
    }


@router.post("/cinemas/{cinema_id}/movies/{movie_id}/movie-times")
def create_movie_time(cinema_id: int, movie_id: int, payload: MovieTimeCreate, db: Session = Depends(get_db)):
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

    hall = (
        db.query(models.Hall)
        .filter(models.Hall.id == payload.hall_id, models.Hall.cinema_id == cinema_id)
        .first()
    )
    if not hall or hall.deleted:
        raise HTTPException(status_code=404, detail="Hall not found")

    mt = models.MovieTime(
        cinema_id=cinema_id,
        hall_id=payload.hall_id,
        movie_id=movie_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        deleted=False
    )
    db.add(mt)
    db.commit()
    db.refresh(mt)
    return {
        "result": MovieTimeResponse.model_validate(mt).model_dump(by_alias=True),
        "errors": [],
        "messages": ["MovieTime created"]
    }

@router.delete("/cinemas/{cinema_id}/movies/{movie_id}/movie-times/{movie_time_id}")
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
