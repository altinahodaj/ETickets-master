import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.db import models
from app.schemas.events import EventCreateModel, EventResponseModel, PhotoModel


router = APIRouter(prefix="/api/cinemas/{cinema_id}/events", tags=["events"])

# GET all events in the database
@router.get("/all", response_model=List[EventResponseModel])
def list_all_events(db: Session = Depends(get_db)):
    events = db.query(models.Event).filter(models.Event.deleted == False).all()
    return events

# GET all events for a cinema
@router.get("", response_model=List[EventResponseModel])
def list_events(cinema_id: int, db: Session = Depends(get_db)):
    events = db.query(models.Event).filter(
        models.Event.cinema_id == cinema_id,
        models.Event.deleted == False
    ).all()
    return events

# GET single event
@router.get("/{event_id}", response_model=EventResponseModel)
def get_event(cinema_id: int, event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(
        models.Event.id == event_id,
        models.Event.cinema_id == cinema_id,
        models.Event.deleted == False
    ).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# CREATE event
@router.post("", response_model=EventResponseModel)
def create_event(cinema_id: int, payload: EventCreateModel, db: Session = Depends(get_db)):
    event = models.Event(
        cinema_id=cinema_id,
        name=payload.name,
        description=payload.description,
        date=payload.date,
        is_paid=payload.is_paid,
        price=payload.price,
        attendees_number=payload.attendees_number,
        deleted=False
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

# UPDATE event
@router.put("/{event_id}", response_model=EventResponseModel)
def update_event(cinema_id: int, event_id: int, payload: EventCreateModel, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(
        models.Event.id == event_id,
        models.Event.cinema_id == cinema_id
    ).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.name = payload.name
    event.description = payload.description
    event.date = payload.date
    event.is_paid = payload.is_paid
    event.price = payload.price
    event.attendees_number = payload.attendees_number

    db.commit()
    db.refresh(event)
    return event

# DELETE event (soft delete)
@router.delete("/{event_id}", response_model=dict)
def delete_event(cinema_id: int, event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(
        models.Event.id == event_id,
        models.Event.cinema_id == cinema_id
    ).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.deleted = True
    db.commit()
    return {"result": True, "message": "Event deleted (soft)"}


# UPLOAD PHOTO for an event
UPLOAD_DIR = "uploads/events"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/{event_id}/photos")
async def upload_event_photo(
    event_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # check if event exists
    event = db.query(models.Event).filter(
        models.Event.id == event_id
    ).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # save file
    filename = f"{event_id}_{file.filename}"
    file_location = os.path.join(UPLOAD_DIR, filename).replace("\\", "/")
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # save record in DB
    # Ruajmë path-in me slashes / që të jetë i pajtueshëm me URL-të
    photo = models.EventPhoto(event_id=event.id, file_path=file_location)
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return {"id": photo.id, "file_path": photo.file_path}


@router.get("/{event_id}/photos")
def list_event_photos(cinema_id: int, event_id: int, db: Session = Depends(get_db)):
    photos = db.query(models.EventPhoto).filter(models.EventPhoto.event_id == event_id).all()
    return [{"id": p.id, "file_path": p.file_path} for p in photos]
