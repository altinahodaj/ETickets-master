from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db import models
from app.db.models import User
from app.db.session import get_db

router = APIRouter(prefix="/api/cinemas/{cinema_id}/halls/{hall_id}", tags=["tickets"])


# ----------------------------
# Schemas
# ----------------------------
class ReserveTicketsDotnetRequest(BaseModel):
    # .NET body: { "ticketsId": [1,2,3], "ownerId": "..." }
    # ownerId do e injorojme sepse e marrim nga tokeni
    ticketsId: list[int]
    ownerId: str | None = None


# ----------------------------
# Read tickets
# ----------------------------
@router.get("/movieTimes/{movie_time_id}/tickets")
def list_tickets(
    cinema_id: int,
    hall_id: int,
    movie_time_id: int,
    db: Session = Depends(get_db),
):
    tickets = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.cinema_id == cinema_id,
            models.Ticket.hall_id == hall_id,
            models.Ticket.movie_time_id == movie_time_id,
            models.Ticket.deleted == False,
        )
        .order_by(models.Ticket.id.asc())
        .all()
    )
    return {"result": tickets, "errors": [], "messages": []}


@router.get("/movieTimes/{movie_time_id}")
def list_tickets_for_movietime(
    cinema_id: int,
    hall_id: int,
    movie_time_id: int,
    db: Session = Depends(get_db),
):
    tickets = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.cinema_id == cinema_id,
            models.Ticket.hall_id == hall_id,
            models.Ticket.movie_time_id == movie_time_id,
            models.Ticket.deleted == False,
        )
        .order_by(models.Ticket.id.asc())
        .all()
    )
    return {"result": tickets, "errors": [], "messages": []}


@router.get("/tickets/{ticket_id}")
def get_ticket(
    cinema_id: int,
    hall_id: int,
    ticket_id: int,
    db: Session = Depends(get_db),
):
    t = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.id == ticket_id,
            models.Ticket.cinema_id == cinema_id,
            models.Ticket.hall_id == hall_id,
            models.Ticket.deleted == False,
        )
        .first()
    )
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {
    "result": {
        "id": t.id,
        "cinema_id": t.cinema_id,
        "hall_id": t.hall_id,
        "movie_time_id": t.movie_time_id,
        "row_id": t.row_id,
        "seat_id": t.seat_id,
        "owner_id": t.owner_id,
        "is_available": t.is_available,
        "is_3d": t.is_3d,
        "is_vip_ticket": t.is_vip_ticket,
        "is_couple_ticket": t.is_couple_ticket,
        "price": t.price,
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "deleted": t.deleted,
    },
    "errors": [],
    "messages": [],
}



# ----------------------------
# Generate tickets (public)
# ----------------------------
@router.post("/movieTimes/{movie_time_id}/generate-tickets")
def generate_tickets(
    cinema_id: int,
    hall_id: int,
    movie_time_id: int,
    db: Session = Depends(get_db),
):
    cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()
    if not cinema or cinema.deleted:
        raise HTTPException(status_code=404, detail="Cinema not found")

    hall = (
        db.query(models.Hall)
        .filter(models.Hall.id == hall_id, models.Hall.cinema_id == cinema_id)
        .first()
    )
    if not hall or hall.deleted:
        raise HTTPException(status_code=404, detail="Hall not found")

    mt = (
        db.query(models.MovieTime)
        .filter(
            models.MovieTime.id == movie_time_id,
            models.MovieTime.cinema_id == cinema_id,
            models.MovieTime.hall_id == hall_id,
        )
        .first()
    )
    if not mt or mt.deleted:
        raise HTTPException(status_code=404, detail="MovieTime not found")

    existing = (
        db.query(models.Ticket)
        .filter(models.Ticket.movie_time_id == movie_time_id, models.Ticket.deleted == False)
        .count()
    )
    if existing > 0:
        raise HTTPException(status_code=400, detail="Tickets already exist for this MovieTime")

    rows = (
        db.query(models.Row)
        .filter(
            models.Row.cinema_id == cinema_id,
            models.Row.hall_id == hall_id,
            models.Row.deleted == False,
        )
        .all()
    )
    row_map = {r.id: r for r in rows}

    seats = (
        db.query(models.Seat)
        .filter(
            models.Seat.cinema_id == cinema_id,
            models.Seat.hall_id == hall_id,
            models.Seat.deleted == False,
        )
        .all()
    )
    if not seats:
        raise HTTPException(status_code=400, detail="No seats found. Generate seating first.")

    created = 0
    for seat in seats:
        row = row_map.get(seat.row_id)
        is_vip = bool(seat.is_vip_seat or (row and row.is_vip_row))
        is_couple = bool(seat.is_couple_seat)
        is_3d = bool(hall.has_3d)

        price = 5
        if is_3d:
            price += 2
        if is_vip:
            price += 3
        if is_couple:
            price += 4

        ticket = models.Ticket(
            cinema_id=cinema_id,
            hall_id=hall_id,
            movie_time_id=movie_time_id,
            row_id=seat.row_id,
            seat_id=seat.id,
            owner_id=None,          # krijohet pa owner
            is_available=True,      # i lire
            is_3d=is_3d,
            is_vip_ticket=is_vip,
            is_couple_ticket=is_couple,
            price=price,
            created_at=datetime.utcnow(),
            deleted=False,
        )
        db.add(ticket)
        created += 1

    db.commit()
    return {"result": {"tickets_created": created}, "errors": [], "messages": ["Tickets generated"]}


# ----------------------------
# Reserve tickets (AUTH REQUIRED) - .NET style route
# ----------------------------
@router.put("/tickets/movieTimes/{movie_time_id}")
def reserve_tickets_dotnet_style(
    cinema_id: int,
    hall_id: int,
    movie_time_id: int,
    payload: ReserveTicketsDotnetRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket_ids = payload.ticketsId
    if not ticket_ids:
        raise HTTPException(status_code=400, detail="ticketsId is required")

    tickets = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.id.in_(ticket_ids),
            models.Ticket.cinema_id == cinema_id,
            models.Ticket.hall_id == hall_id,
            models.Ticket.movie_time_id == movie_time_id,
            models.Ticket.deleted == False,
        )
        .all()
    )

    if len(tickets) != len(ticket_ids):
        raise HTTPException(status_code=404, detail="One or more tickets not found")

    # kontrollo nese jane te lira
    for t in tickets:
        if not t.is_available or t.owner_id is not None:
            raise HTTPException(status_code=400, detail=f"Ticket {t.id} is already reserved")

    # rezervim: owner_id merret nga token
    for t in tickets:
        t.is_available = False
        t.owner_id = current_user.id

    db.commit()

    result = [
        {
            "id": t.id,
            "cinema_id": t.cinema_id,
            "hall_id": t.hall_id,
            "movie_time_id": t.movie_time_id,
            "row_id": t.row_id,
            "seat_id": t.seat_id,
            "owner_id": t.owner_id,
            "is_available": t.is_available,
            "is_3d": t.is_3d,
            "is_vip_ticket": t.is_vip_ticket,
            "is_couple_ticket": t.is_couple_ticket,
            "price": t.price,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "deleted": t.deleted,
        }
        for t in tickets
    ]

    return {"result": result, "errors": [], "messages": ["Tickets reserved successfully"]}



# ----------------------------
# My tickets (AUTH REQUIRED)
# (si .NET: user-i i kycur sheh biletat e veta)
# ----------------------------
@router.get("/my-tickets")
def my_tickets(
    cinema_id: int,
    hall_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tickets = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.cinema_id == cinema_id,
            models.Ticket.hall_id == hall_id,
            models.Ticket.owner_id == current_user.id,
            models.Ticket.deleted == False,
        )
        .order_by(models.Ticket.id.asc())
        .all()
    )
    return {"result": tickets, "errors": [], "messages": []}
