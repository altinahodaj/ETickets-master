from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models

router = APIRouter(prefix="/api/cinemas", tags=["cinemas"])


def cinema_to_dict(c: models.Cinema):
    return {
        "id": c.id,
        "name": c.name,
        "city": c.city,
        "address": c.address,
        "description": c.description,
        "deleted": c.deleted,
        "photos": [
            {
                "id": p.id,
                "cinemaId": p.cinema_id,
                "movieId": p.movie_id,
                "photoType": p.photo_type,
                "name": p.name,
                "imgPath": p.img_path,
                "imgClientPath": p.img_client_path,
                "description": p.description,
            }
            for p in (c.photos or [])
        ],
    }


@router.get("")
def list_cinemas(db: Session = Depends(get_db)):
    cinemas = (
        db.query(models.Cinema)
        .filter(models.Cinema.deleted == False)
        .all()
    )
    return {"result": [cinema_to_dict(c) for c in cinemas], "errors": [], "messages": []}


@router.get("/{cinema_id}")
def get_cinema(cinema_id: int, db: Session = Depends(get_db)):
    cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()
    if not cinema or cinema.deleted:
        raise HTTPException(status_code=404, detail="Cinema not found")
    return {"result": cinema_to_dict(cinema), "errors": [], "messages": []}


@router.post("")
def create_cinema(payload: dict, db: Session = Depends(get_db)):
    name = payload.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="name is required")

    cinema = models.Cinema(
        name=name,
        city=payload.get("city"),
        address=payload.get("address"),
        description=payload.get("description"),
        deleted=False,
    )
    db.add(cinema)
    db.commit()
    db.refresh(cinema)
    return {"result": cinema_to_dict(cinema), "errors": [], "messages": ["Cinema created"]}


@router.put("/{cinema_id}")
def update_cinema(cinema_id: int, payload: dict, db: Session = Depends(get_db)):
    cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(status_code=404, detail="Cinema not found")

    for field in ["name", "city", "address", "description", "deleted"]:
        if field in payload:
            setattr(cinema, field, payload[field])

    db.commit()
    db.refresh(cinema)
    return {"result": cinema_to_dict(cinema), "errors": [], "messages": ["Cinema updated"]}


@router.delete("/{cinema_id}")
def delete_cinema(cinema_id: int, db: Session = Depends(get_db)):
    cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(status_code=404, detail="Cinema not found")

    cinema.deleted = True
    db.commit()
    return {"result": True, "errors": [], "messages": ["Cinema deleted (soft)"]}
