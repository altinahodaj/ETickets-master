from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models

router = APIRouter(prefix="/api/cinemas/{cinema_id}/halls/{hall_id}", tags=["seating"])

@router.get("/rows")
def list_rows(cinema_id: int, hall_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(models.Row)
        .filter(
            models.Row.cinema_id == cinema_id,
            models.Row.hall_id == hall_id,
            models.Row.deleted == False
        )
        .order_by(models.Row.id.asc())
        .all()
    )
    return {"result": rows, "errors": [], "messages": []}

@router.get("/rows/{row_id}/seats")
def list_seats_in_row(cinema_id: int, hall_id: int, row_id: int, db: Session = Depends(get_db)):
    seats = (
        db.query(models.Seat)
        .filter(
            models.Seat.cinema_id == cinema_id,
            models.Seat.hall_id == hall_id,
            models.Seat.row_id == row_id,
            models.Seat.deleted == False
        )
        .order_by(models.Seat.id.asc())
        .all()
    )
    return {"result": seats, "errors": [], "messages": []}

@router.post("/generate-seating")
def generate_seating(cinema_id: int, hall_id: int, payload: dict, db: Session = Depends(get_db)):
    """
    payload example:
    {
      "rows": 5,
      "seats_per_row": 10,
      "vip_rows": ["A"],
      "vip_seats": ["A1","A2"],
      "couple_seats": ["B9","B10"]
    }
    """
    # kontrollo cinema/hall
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

    rows_count = payload.get("rows")
    seats_per_row = payload.get("seats_per_row")
    if not rows_count or not seats_per_row:
        raise HTTPException(status_code=400, detail="rows and seats_per_row are required")

    vip_rows = set(payload.get("vip_rows", []))
    vip_seats = set(payload.get("vip_seats", []))
    couple_seats = set(payload.get("couple_seats", []))

    # mos krijo dy herë nëse ka seating ekzistues
    existing_rows = (
        db.query(models.Row)
        .filter(models.Row.cinema_id == cinema_id, models.Row.hall_id == hall_id, models.Row.deleted == False)
        .count()
    )
    if existing_rows > 0:
        raise HTTPException(status_code=400, detail="This hall already has rows. Delete them first or use another hall.")

    created_rows = 0
    created_seats = 0

    # A, B, C, ...
    for i in range(rows_count):
        row_letter = chr(ord("A") + i)  # 0->A,1->B,...

        row = models.Row(
            cinema_id=cinema_id,
            hall_id=hall_id,
            row_name=row_letter,
            number_of_seats=seats_per_row,
            is_vip_row=(row_letter in vip_rows),
            deleted=False
        )
        db.add(row)
        db.flush()  # merr row.id pa commit

        created_rows += 1

        for s in range(1, seats_per_row + 1):
            seat_name = f"{row_letter}{s}"  # p.sh A1
            seat = models.Seat(
                cinema_id=cinema_id,
                hall_id=hall_id,
                row_id=row.id,
                seat_name=seat_name,
                is_vip_seat=(seat_name in vip_seats),
                is_couple_seat=(seat_name in couple_seats),
                deleted=False
            )
            db.add(seat)
            created_seats += 1

    db.commit()
    return {"result": {"rows_created": created_rows, "seats_created": created_seats}, "errors": [], "messages": ["Seating generated"]}
