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
# Ticket pricing (OOP: inheritance + polymorphism)
# ----------------------------
class BasePricer:
    def calculate(self, *, base_price: int, is_3d: bool) -> int:
        price = base_price
        if is_3d:
            price += 2
        return price


class AddonPricer(BasePricer):
    def __init__(self, addon_amount: int = 0) -> None:
        self.addon_amount = addon_amount

    def calculate(self, *, base_price: int, is_3d: bool) -> int:
        price = super().calculate(base_price=base_price, is_3d=is_3d)
        return price + self.addon_amount


class VipAddonPricer(AddonPricer):
    addon_amount = 3


class CoupleAddonPricer(AddonPricer):
    addon_amount = 4


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

        pricer: BasePricer
        if is_vip and is_couple:
            pricer = AddonPricer(addon_amount=7)
        elif is_vip:
            pricer = VipAddonPricer()
        elif is_couple:
            pricer = CoupleAddonPricer()
        else:
            pricer = BasePricer()

        price = pricer.calculate(base_price=5, is_3d=is_3d)

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
):
    ticket_ids = payload.ticketsId
    if not ticket_ids:
        raise HTTPException(status_code=400, detail="ticketsId is required")

    owner_id = (payload.ownerId or "").strip() if payload.ownerId else None
    if not owner_id:
        raise HTTPException(status_code=400, detail="ownerId is required")

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

    # rezervim: owner_id merret nga payload (Firebase UID)
    reserved_at = datetime.utcnow()
    for t in tickets:
        t.is_available = False
        t.owner_id = owner_id
        # Use created_at as "reservation time" for UI grouping (last purchase)
        t.created_at = reserved_at

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
# User tickets (PUBLIC)
# Frontend expects: /api/cinemas/0/halls/0/user-tickets/{userId}
# If cinema_id/hall_id are 0, return all tickets for the user.
# ----------------------------
@router.get("/user-tickets/{user_id}")
def user_tickets(
    cinema_id: int,
    hall_id: int,
    user_id: str,
    db: Session = Depends(get_db),
):
    q = (
        db.query(
            models.Ticket,
            models.Seat,
            models.Row,
            models.MovieTime,
            models.Hall,
            models.Movie,
            models.Cinema,
        )
        .join(models.Seat, models.Seat.id == models.Ticket.seat_id)
        .join(models.Row, models.Row.id == models.Ticket.row_id)
        .join(models.MovieTime, models.MovieTime.id == models.Ticket.movie_time_id)
        .join(models.Hall, models.Hall.id == models.Ticket.hall_id)
        .join(models.Movie, models.Movie.id == models.MovieTime.movie_id)
        .join(models.Cinema, models.Cinema.id == models.Ticket.cinema_id)
        .filter(
            models.Ticket.owner_id == user_id,
            models.Ticket.deleted == False,
        )
    )

    if cinema_id and cinema_id != 0:
        q = q.filter(models.Ticket.cinema_id == cinema_id)
    if hall_id and hall_id != 0:
        q = q.filter(models.Ticket.hall_id == hall_id)

    rows = q.order_by(models.Ticket.created_at.desc()).all()

    result = []
    for t, seat, row, mt, hall, movie, cinema in rows:
        item = {
            # ids
            "id": t.id,
            "cinemaId": t.cinema_id,
            "hallId": t.hall_id,
            "movieTimeId": t.movie_time_id,
            "rowId": t.row_id,
            "seatId": t.seat_id,

            # display helpers
            "cinemaName": getattr(cinema, "name", None),
            "hallName": getattr(hall, "name", None),
            "hallNumber": getattr(hall, "hall_number", None),
            "movieTitle": getattr(movie, "title", None),
            "rowName": getattr(row, "row_name", None),
            "seatName": getattr(seat, "seat_name", None),

            # ticket
            "ticketCode": t.ticket_code,
            "ownerId": t.owner_id,
            "isAvailable": t.is_available,
            "is3D": t.is_3d,
            "isVipTicket": t.is_vip_ticket,
            "isCoupleTicket": t.is_couple_ticket,
            "price": t.price,
            "createdAt": t.created_at.isoformat() if t.created_at else None,

            # movie time
            "movieStartTime": mt.start_time.isoformat() if mt and mt.start_time else None,
            "movieEndTime": mt.end_time.isoformat() if mt and mt.end_time else None,
        }

        # also include snake_case for older consumers
        item.update(
            {
                "cinema_id": t.cinema_id,
                "hall_id": t.hall_id,
                "movie_time_id": t.movie_time_id,
                "row_id": t.row_id,
                "seat_id": t.seat_id,
                "ticket_code": t.ticket_code,
                "owner_id": t.owner_id,
                "is_available": t.is_available,
                "is_3d": t.is_3d,
                "is_vip_ticket": t.is_vip_ticket,
                "is_couple_ticket": t.is_couple_ticket,
                "created_at": t.created_at.isoformat() if t.created_at else None,
                "row_name": getattr(row, "row_name", None),
                "seat_name": getattr(seat, "seat_name", None),
                "movie_start_time": mt.start_time.isoformat() if mt and mt.start_time else None,
                "movie_end_time": mt.end_time.isoformat() if mt and mt.end_time else None,
            }
        )

        result.append(item)

    return {"result": result, "errors": [], "messages": []}



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
