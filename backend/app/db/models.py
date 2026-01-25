import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    ForeignKey,
    Text,
    DateTime,
    UniqueConstraint,
    and_,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True, unique=True, index=True)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    cinema_id: Mapped[int | None] = mapped_column(ForeignKey("cinemas.id"), nullable=True)
    movie_id: Mapped[int | None] = mapped_column(ForeignKey("movies.id"), nullable=True)
    actor_id: Mapped[int | None] = mapped_column(ForeignKey("actors.id"), nullable=True) 

    # p.sh. "cinema" | "movie" | "banner" | "actors"
    photo_type: Mapped[str] = mapped_column(String(50), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    img_path: Mapped[str] = mapped_column(String(500), nullable=False)
    img_client_path: Mapped[str] = mapped_column(String(500), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    insert_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Cinema(Base):
    __tablename__ = "cinemas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    address: Mapped[str | None] = mapped_column(String(250), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    movies: Mapped[list["Movie"]] = relationship(
        back_populates="cinema",
        cascade="all, delete-orphan",
    )

    # photos të kinemas (cinema_id set + movie_id NULL + photo_type='cinema')
    photos: Mapped[list["Photo"]] = relationship(
        "Photo",
        primaryjoin=lambda: and_(
            Cinema.id == Photo.cinema_id,
            Photo.movie_id.is_(None),
            Photo.photo_type == "cinema",
            Photo.deleted == False,
        ),
        viewonly=True,
        order_by=lambda: Photo.insert_date.desc(),
        lazy="selectin",
    )


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    genre: Mapped[str | None] = mapped_column(String(120), nullable=True)
    language: Mapped[str | None] = mapped_column(String(120), nullable=True)
    length_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # ✅ SHTESAT
    release_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    director: Mapped[str | None] = mapped_column(String(200), nullable=True)

    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    cinema: Mapped["Cinema"] = relationship(back_populates="movies")

    # photos të filmit (movie_id set + photo_type='movie' ose 'banner' + deleted=false)
    photos: Mapped[list["Photo"]] = relationship(
        "Photo",
        primaryjoin=lambda: and_(
            Movie.id == Photo.movie_id,
            Photo.deleted == False,
        ),
        viewonly=True,
        order_by=lambda: Photo.insert_date.desc(),
        lazy="selectin",
    )

    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        primaryjoin="and_(Movie.id==Review.movie_id, Review.deleted==False)",
        viewonly=True,
        order_by="desc(Review.insert_date)",
        lazy="selectin",
    )


class Review(Base):
    __tablename__ = "movie_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)

    review_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    review_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    review_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)

    user_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_name: Mapped[str | None] = mapped_column(String(150), nullable=True)

    insert_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class Hall(Base):
    __tablename__ = "halls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    hall_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    number_of_rows: Mapped[int | None] = mapped_column(Integer, nullable=True)
    has_3d: Mapped[bool] = mapped_column(Boolean, default=False)

    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    rows: Mapped[list["Row"]] = relationship("Row", back_populates="hall", lazy="selectin")


class MovieTime(Base):
    __tablename__ = "movie_times"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id"), nullable=False)
    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id"), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)

    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    hall: Mapped["Hall"] = relationship(lazy="selectin")


class Row(Base):
    __tablename__ = "rows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id"), nullable=False)
    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id"), nullable=False)

    row_name: Mapped[str] = mapped_column(String(50), nullable=False)
    number_of_seats: Mapped[int] = mapped_column(Integer, nullable=False)
    is_vip_row: Mapped[bool] = mapped_column(Boolean, default=False)

    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    hall: Mapped["Hall"] = relationship("Hall", back_populates="rows")
    seats: Mapped[list["Seat"]] = relationship("Seat", back_populates="row", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("hall_id", "row_name", name="uq_rows_hall_rowname"),
    )


class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id"), nullable=False)
    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id"), nullable=False)
    row_id: Mapped[int] = mapped_column(ForeignKey("rows.id"), nullable=False)

    seat_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_vip_seat: Mapped[bool] = mapped_column(Boolean, default=False)
    is_couple_seat: Mapped[bool] = mapped_column(Boolean, default=False)

    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    row: Mapped["Row"] = relationship("Row", back_populates="seats")

    __table_args__ = (
        UniqueConstraint("row_id", "seat_name", name="uq_seats_row_seatname"),
    )


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id"), nullable=False)
    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id"), nullable=False)
    movie_time_id: Mapped[int] = mapped_column(ForeignKey("movie_times.id"), nullable=False)

    row_id: Mapped[int] = mapped_column(ForeignKey("rows.id"), nullable=False)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"), nullable=False)

    ticket_code: Mapped[str] = mapped_column(
        String(36), unique=True, default=lambda: str(uuid.uuid4())
    )
    owner_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    is_3d: Mapped[bool] = mapped_column(Boolean, default=False)
    is_vip_ticket: Mapped[bool] = mapped_column(Boolean, default=False)
    is_couple_ticket: Mapped[bool] = mapped_column(Boolean, default=False)

    price: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint("movie_time_id", "seat_id", name="uq_ticket_movietime_seat"),
    )


class Actor(Base):
    __tablename__ = "actors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    img_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(100), nullable=True)
    genre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    birth: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    photos: Mapped[list["Photo"]] = relationship(
        "Photo",
        primaryjoin=lambda: and_(
            Actor.id == Photo.actor_id,
            Photo.photo_type == "actor",
            Photo.deleted == False,
        ),
        viewonly=True,
        order_by=lambda: Photo.insert_date.desc(),
        lazy="selectin",
    )


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    price: Mapped[int] = mapped_column(Integer, default=0)
    attendees_number: Mapped[int] = mapped_column(Integer, default=0)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    photos: Mapped[list["EventPhoto"]] = relationship(
        "EventPhoto",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete-orphan"
    )


class EventPhoto(Base):
    __tablename__ = "event_photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)

    event: Mapped["Event"] = relationship(back_populates="photos")

    