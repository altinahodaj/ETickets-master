# backend/app/routers/events.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models

router = APIRouter(prefix="/api", tags=["events"])

# ✅ kjo është URL bazë e backend-it (si e ke në local)
BASE_URL = "http://127.0.0.1:8000"


def _assets_events_dir() -> Path:
    # events.py -> routers -> app -> backend -> ROOT
    root_dir = Path(__file__).resolve().parents[3]
    assets_dir = root_dir / "assets" / "app_files" / "Events"
    assets_dir.mkdir(parents=True, exist_ok=True)
    return assets_dir



def _to_event_dict(e: models.Event) -> dict:
    return {
        "id": e.id,
        "cinemaId": e.cinema_id,
        "title": e.title,
        "description": e.description,
        "eventDate": e.event_date.isoformat() if e.event_date else None,

        # path relativ i ruajtur në DB
        "imagePath": e.image_path,

        # URL për frontend
        "imgClientPath": (
            f"http://127.0.0.1:8000/assets/{e.image_path}"
            if e.image_path
            else None
        ),

        "deleted": e.deleted,
    }


@router.get("/events")
def list_events(db: Session = Depends(get_db)):
    events = (
        db.query(models.Event)
        .filter(models.Event.deleted == False)  # noqa: E712
        .order_by(models.Event.event_date.asc())
        .all()
    )
    return {"result": [_to_event_dict(e) for e in events], "errors": [], "messages": []}


@router.get("/cinemas/{cinema_id}/events")
def list_events_by_cinema(cinema_id: int, db: Session = Depends(get_db)):
    events = (
        db.query(models.Event)
        .filter(
            models.Event.cinema_id == cinema_id,
            models.Event.deleted == False,  # noqa: E712
        )
        .order_by(models.Event.event_date.asc())
        .all()
    )
    return {"result": [_to_event_dict(e) for e in events], "errors": [], "messages": []}


@router.get("/cinemas/{cinema_id}/events/{event_id}")
def get_event(cinema_id: int, event_id: int, db: Session = Depends(get_db)):
    e = (
        db.query(models.Event)
        .filter(
            models.Event.id == event_id,
            models.Event.cinema_id == cinema_id,
            models.Event.deleted == False,  # noqa: E712
        )
        .first()
    )

    if not e:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"result": _to_event_dict(e), "errors": [], "messages": []}


@router.post("/cinemas/{cinema_id}/events")
def create_event(
    cinema_id: int,
    title: str,
    description: Optional[str] = None,
    eventDate: Optional[str] = None,  # ISO string
    db: Session = Depends(get_db),
):
    cinema = (
        db.query(models.Cinema)
        .filter(models.Cinema.id == cinema_id, models.Cinema.deleted == False)  # noqa: E712
        .first()
    )
    if not cinema:
        raise HTTPException(status_code=404, detail="Cinema not found")

    if eventDate:
        try:
            dt = datetime.fromisoformat(eventDate.replace("Z", "+00:00"))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid eventDate (use ISO format)")
    else:
        dt = datetime.now()

    e = models.Event(
        cinema_id=cinema_id,
        title=title,
        description=description,
        event_date=dt,
        image_path=None,  # ✅ do ta mbushim pas upload-it
        deleted=False,
    )
    db.add(e)
    db.commit()
    db.refresh(e)

    return {"result": _to_event_dict(e), "errors": [], "messages": ["Event created"]}


@router.post("/cinemas/{cinema_id}/events/{event_id}/photo")
async def upload_event_photo(
    cinema_id: int,
    event_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    e = (
        db.query(models.Event)
        .filter(
            models.Event.id == event_id,
            models.Event.cinema_id == cinema_id,
            models.Event.deleted == False,  # noqa: E712
        )
        .first()
    )
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    ext = Path(file.filename).suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise HTTPException(status_code=400, detail="Only .jpg/.jpeg/.png/.webp allowed")

    filename = f"{uuid4().hex}{ext}"

    # backend/assets/app_files/Events/<filename>
    dest = _assets_events_dir() / filename

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    dest.write_bytes(content)

    # ✅ RUJE path RELATIV (që shërbehet nga /assets)
    # /assets -> backend/assets
    e.image_path = f"app_files/Events/{filename}"

    db.add(e)
    db.commit()
    db.refresh(e)

    return {"result": _to_event_dict(e), "errors": [], "messages": ["Photo uploaded"]}


@router.delete("/cinemas/{cinema_id}/events/{event_id}")
def delete_event(cinema_id: int, event_id: int, db: Session = Depends(get_db)):
    e = (
        db.query(models.Event)
        .filter(models.Event.id == event_id, models.Event.cinema_id == cinema_id)
        .first()
    )
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")

    e.deleted = True
    db.add(e)
    db.commit()

    return {"result": True, "errors": [], "messages": ["Event deleted"]}
