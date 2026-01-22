from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models

router = APIRouter(prefix="/api/actors", tags=["actors"])


# ------------------------------
# Helper to serialize actor objects
# ------------------------------
def actor_to_dict(a: models.Actor):
    return {
        "id": a.id,
        "firstName": a.first_name,
        "lastName": a.last_name,
        "imgPath": a.img_path,       # main image
        "nationality": a.nationality,
        "genre": a.genre,
        "birth": a.birth.isoformat() if a.birth else None,
        "deleted": a.deleted,
        "photos": [p.img_client_path for p in (a.photos or [])],  # only frontend path
    }


# ------------------------------
# LIST ALL ACTORS
# ------------------------------
@router.get("")
def list_actors(db: Session = Depends(get_db)):
    actors = db.query(models.Actor).filter(models.Actor.deleted == False).all()
    return {"result": [actor_to_dict(a) for a in actors], "errors": [], "messages": []}


# ------------------------------
# GET SINGLE ACTOR
# ------------------------------
@router.get("/{actor_id}")
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor or actor.deleted:
        raise HTTPException(status_code=404, detail="Actor not found")
    return {"result": actor_to_dict(actor), "errors": [], "messages": []}


# ------------------------------
# CREATE ACTOR
# ------------------------------
@router.post("")
def create_actor(payload: dict, db: Session = Depends(get_db)):
    first_name = payload.get("firstName")
    last_name = payload.get("lastName")
    if not first_name or not last_name:
        raise HTTPException(status_code=400, detail="firstName and lastName are required")

    actor = models.Actor(
        first_name=first_name,
        last_name=last_name,
        img_path=payload.get("imgPath"),
        nationality=payload.get("nationality"),
        genre=payload.get("genre"),
        birth=payload.get("birth"),
        deleted=False,
    )
    db.add(actor)
    db.commit()
    db.refresh(actor)
    return {"result": actor_to_dict(actor), "errors": [], "messages": ["Actor created"]}


# ------------------------------
# UPDATE ACTOR
# ------------------------------
@router.put("/{actor_id}")
def update_actor(actor_id: int, payload: dict, db: Session = Depends(get_db)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    for field in ["first_name", "last_name", "img_path", "nationality", "genre", "birth", "deleted"]:
        frontend_field = field
        if field == "first_name": frontend_field = "firstName"
        if field == "last_name": frontend_field = "lastName"
        if field == "img_path": frontend_field = "imgPath"

        if frontend_field in payload:
            setattr(actor, field, payload[frontend_field])

    db.commit()
    db.refresh(actor)
    return {"result": actor_to_dict(actor), "errors": [], "messages": ["Actor updated"]}


# ------------------------------
# DELETE ACTOR (soft delete)
# ------------------------------
@router.delete("/{actor_id}")
def delete_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    actor.deleted = True
    db.commit()
    return {"result": True, "errors": [], "messages": ["Actor deleted (soft)"]}
