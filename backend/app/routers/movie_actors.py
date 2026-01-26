from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.db import models

router = APIRouter(prefix="/api", tags=["movie-actors"])


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
            {"id": p.id, "imgClientPath": p.img_client_path}
            for p in (a.photos or [])
        ],
    }


@router.get("/cinemas/{cinema_id}/movies/{movie_id}/actors", response_model=dict)
def get_movie_actors(cinema_id: int, movie_id: int, db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .options(joinedload(models.Movie.actors).joinedload(models.Actor.photos))
        .filter(
            models.Movie.id == movie_id,
            models.Movie.cinema_id == cinema_id,
            models.Movie.deleted == False,
        )
        .first()
    )

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {
        "result": [actor_to_dict(a) for a in (movie.actors or [])],
        "errors": [],
        "messages": [],
    }
