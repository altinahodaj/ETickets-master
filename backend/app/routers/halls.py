from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from app.db import models
from app.schemas.halls import HallResponse

router = APIRouter(prefix="/api/cinemas/{cinema_id}/halls", tags=["halls"])

@router.get("", response_model=dict)
def list_halls(cinema_id: int, db: Session = Depends(get_db)):
    cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()
    if not cinema or cinema.deleted:
        raise HTTPException(status_code=404, detail="Cinema not found")

    halls = (
        db.query(models.Hall)
        .options(joinedload(models.Hall.rows).joinedload(models.Row.seats))
        .filter(models.Hall.cinema_id == cinema_id, models.Hall.deleted == False)
        .all()
    )
    result = [HallResponse.model_validate(h).model_dump(by_alias=True) for h in halls]
    return {"result": result, "errors": [], "messages": []}

@router.get("/{hall_id}", response_model=dict)
def get_hall(cinema_id: int, hall_id: int, db: Session = Depends(get_db)):
    hall = (
        db.query(models.Hall)
        .options(joinedload(models.Hall.rows).joinedload(models.Row.seats))
        .filter(
            models.Hall.id == hall_id,
            models.Hall.cinema_id == cinema_id
        )
        .first()
    )
    if not hall or hall.deleted:
        raise HTTPException(status_code=404, detail="Hall not found")

    return {
        "result": HallResponse.model_validate(hall).model_dump(by_alias=True),
        "errors": [],
        "messages": []
    }

@router.post("")
def create_hall(cinema_id: int, payload: dict, db: Session = Depends(get_db)):
    cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()
    if not cinema or cinema.deleted:
        raise HTTPException(status_code=404, detail="Cinema not found")

    name = payload.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="name is required")

    hall = models.Hall(
        cinema_id=cinema_id,
        name=name,
        hall_number=payload.get("hall_number"),
        number_of_rows=payload.get("number_of_rows"),
        has_3d=payload.get("has_3d", False),
        deleted=False
    )
    db.add(hall)
    db.commit()
    db.refresh(hall)
    return {"result": hall, "errors": [], "messages": ["Hall created"]}

@router.put("/{hall_id}")
def update_hall(cinema_id: int, hall_id: int, payload: dict, db: Session = Depends(get_db)):
    hall = (
        db.query(models.Hall)
        .filter(models.Hall.id == hall_id, models.Hall.cinema_id == cinema_id)
        .first()
    )
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")

    for field in ["name", "hall_number", "number_of_rows", "has_3d", "deleted"]:
        if field in payload:
            setattr(hall, field, payload[field])

    db.commit()
    db.refresh(hall)
    return {"result": hall, "errors": [], "messages": ["Hall updated"]}

@router.delete("/{hall_id}")
def delete_hall(cinema_id: int, hall_id: int, db: Session = Depends(get_db)):
    hall = (
        db.query(models.Hall)
        .filter(models.Hall.id == hall_id, models.Hall.cinema_id == cinema_id)
        .first()
    )
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")

    hall.deleted = True
    db.commit()
    return {"result": True, "errors": [], "messages": ["Hall deleted (soft)"]}
