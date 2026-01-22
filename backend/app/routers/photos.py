import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.db import models

router = APIRouter(prefix="/api/cinemas/{cinema_id}", tags=["photos"])


def api_response(result=None, success=True, errors=None, messages=None):
    return {
        "success": success,
        "errors": errors or [],
        "messages": messages or [],
        "result": result,
    }


def get_assets_root() -> Path:
    # app/routers/photos.py -> backend/
    base_dir = Path(__file__).resolve().parent.parent.parent
    return base_dir / "assets" / "app_files"


def save_files(files: List[UploadFile], folder_name: str) -> List[tuple[str, Path]]:
    assets_root = get_assets_root()
    target_dir = assets_root / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    saved: List[tuple[str, Path]] = []
    for f in files:
        ext = Path(f.filename).suffix.lower()
        new_name = f"{uuid.uuid4()}{ext}"
        abs_path = target_dir / new_name

        with open(abs_path, "wb") as out:
            out.write(f.file.read())

        saved.append((new_name, abs_path))

    return saved


def photo_to_dict(p: models.Photo):
    return {
        "id": p.id,
        "cinemaId": p.cinema_id,
        "movieId": p.movie_id,
        "photoType": p.photo_type,
        "name": p.name,
        "imgPath": p.img_path,
        "imgClientPath": p.img_client_path,
        "description": p.description,
    }



@router.get("/photos")
def get_cinema_photos(cinema_id: int, db: Session = Depends(get_db)):
    cinema = (
        db.query(models.Cinema)
        .filter(models.Cinema.id == cinema_id, models.Cinema.deleted == False)
        .first()
    )
    if not cinema:
        raise HTTPException(status_code=404, detail="Cinema not found")

    photos = (
        db.query(models.Photo)
        .filter(
            models.Photo.cinema_id == cinema_id,
            models.Photo.movie_id == None,
            models.Photo.photo_type == "cinema",
            models.Photo.deleted == False,
        )
        .all()
    )
    return api_response([photo_to_dict(p) for p in photos])


@router.post("/photos", status_code=201)
def upload_cinema_photos(
    cinema_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    cinema = (
        db.query(models.Cinema)
        .filter(models.Cinema.id == cinema_id, models.Cinema.deleted == False)
        .first()
    )
    if not cinema:
        raise HTTPException(status_code=404, detail="Cinema not found")

    saved = save_files(files, "Cinemas")

    created: list[models.Photo] = []
    for filename, abs_path in saved:
        client_url = f"{settings.STATIC_BASE_URL}/assets/app_files/Cinemas/{filename}"

        p = models.Photo(
            cinema_id=cinema_id,
            movie_id=None,
            photo_type="cinema",
            name=filename,
            img_path=str(abs_path),
            img_client_path=client_url,
            description=None,
            deleted=False,
        )
        db.add(p)
        created.append(p)

    db.commit()
    for p in created:
        db.refresh(p)

    return api_response(
        [photo_to_dict(p) for p in created],
        messages=["Cinema photos uploaded"],
    )


@router.delete("/photos/{photo_id}")
def delete_cinema_photo(cinema_id: int, photo_id: str, db: Session = Depends(get_db)):
    p = (
        db.query(models.Photo)
        .filter(
            models.Photo.id == photo_id,
            models.Photo.cinema_id == cinema_id,
            models.Photo.movie_id == None,
            models.Photo.photo_type == "cinema",
            models.Photo.deleted == False,
        )
        .first()
    )
    if not p:
        raise HTTPException(status_code=404, detail="Photo not found")

    p.deleted = True
    db.commit()
    return api_response(photo_to_dict(p), messages=["Cinema photo deleted"])


@router.get("/movies/{movie_id}/photos")
def get_movie_photos(cinema_id: int, movie_id: int, db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .filter(
            models.Movie.id == movie_id,
            models.Movie.cinema_id == cinema_id,
            models.Movie.deleted == False,
        )
        .first()
    )
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    photos = (
        db.query(models.Photo)
        .filter(
            models.Photo.cinema_id == cinema_id,
            models.Photo.movie_id == movie_id,
            models.Photo.photo_type == "movie",
            models.Photo.deleted == False,
        )
        .all()
    )

    return api_response([photo_to_dict(p) for p in photos])


@router.post("/movies/{movie_id}/photos", status_code=201)
def upload_movie_photos(
    cinema_id: int,
    movie_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    movie = (
        db.query(models.Movie)
        .filter(
            models.Movie.id == movie_id,
            models.Movie.cinema_id == cinema_id,
            models.Movie.deleted == False,
        )
        .first()
    )
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    saved = save_files(files, "Movies")

    created: list[models.Photo] = []
    for filename, abs_path in saved:
        client_url = f"{settings.STATIC_BASE_URL}/assets/app_files/Movies/{filename}"

        p = models.Photo(
            cinema_id=cinema_id,
            movie_id=movie_id,
            photo_type="movie",
            name=filename,
            img_path=str(abs_path),
            img_client_path=client_url,
            description=None,
            deleted=False,
        )
        db.add(p)
        created.append(p)

    db.commit()
    for p in created:
        db.refresh(p)

    return api_response(
        [photo_to_dict(p) for p in created],
        messages=["Movie photos uploaded"],
    )


@router.delete("/movies/{movie_id}/photos/{photo_id}")
def delete_movie_photo(cinema_id: int, movie_id: int, photo_id: str, db: Session = Depends(get_db)):
    p = (
        db.query(models.Photo)
        .filter(
            models.Photo.id == photo_id,
            models.Photo.cinema_id == cinema_id,
            models.Photo.movie_id == movie_id,
            models.Photo.photo_type == "movie",
            models.Photo.deleted == False,
        )
        .first()
    )

    if not p:
        raise HTTPException(status_code=404, detail="Photo not found")

    p.deleted = True
    db.commit()

    return api_response(photo_to_dict(p), messages=["Movie photo deleted"])
