from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

from app.db.session import get_db
from app.db import models
from app.schemas.actors import ActorCreate

router = APIRouter(prefix="/api/actors", tags=["actors"])


class ApiResponse(BaseModel):
    result: Optional[object] = None
    errors: List[str] = Field(default_factory=list)
    messages: List[str] = Field(default_factory=list)


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


@router.get("", response_model=ApiResponse)
def list_actors(db: Session = Depends(get_db)):
    actors = db.query(models.Actor).filter(models.Actor.deleted == False).all()
    return {"result": [actor_to_dict(a) for a in actors], "errors": [], "messages": []}


@router.get("/{actor_id}", response_model=ApiResponse)
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor or actor.deleted:
        raise HTTPException(status_code=404, detail="Actor not found")
    return {"result": actor_to_dict(actor), "errors": [], "messages": []}


@router.post("", response_model=ApiResponse)
def create_actor(payload: ActorCreate, db: Session = Depends(get_db)):
    actor = models.Actor(
        first_name=payload.firstName,
        last_name=payload.lastName,
        img_path=payload.imgPath,
        nationality=payload.nationality,
        genre=payload.genre,
        birth=payload.birth,
        deleted=False,
    )
    db.add(actor)
    db.commit()
    db.refresh(actor)
    return {"result": actor_to_dict(actor), "errors": [], "messages": ["Actor created"]}


@router.put("/{actor_id}", response_model=ApiResponse)
def update_actor(actor_id: int, payload: ActorCreate, db: Session = Depends(get_db)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    actor.first_name = payload.firstName
    actor.last_name = payload.lastName
    actor.img_path = payload.imgPath
    actor.nationality = payload.nationality
    actor.genre = payload.genre
    actor.birth = payload.birth

    db.commit()
    db.refresh(actor)
    return {"result": actor_to_dict(actor), "errors": [], "messages": ["Actor updated"]}


@router.delete("/{actor_id}", response_model=ApiResponse)
def delete_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    actor.deleted = True
    db.commit()
    return {"result": True, "errors": [], "messages": ["Actor deleted (soft)"]}
