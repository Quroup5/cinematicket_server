import sqlalchemy as db
from sqlalchemy.orm import relationship
from datetime import datetime
from config.settings import Base

cinema_film = db.Table(
    "cinema_film",
    Base.metadata,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column("id_cinema", db.Integer, db.ForeignKey("cinemas.id")),
    db.Column("id_film", db.Integer, db.ForeignKey("films.id")),
)


cinema_showtime = db.Table(
    "cinema_showtime",
    Base.metadata,
    db.Column("id_cinema", db.Integer, db.ForeignKey("cinemas.id")),
    db.Column("id_showtime", db.Integer, db.ForeignKey("showtimes.id")),
)

seat_showtime = db.Table(
    "seat_showtime",
    Base.metadata,
    db.Column("id_seat", db.Integer, db.ForeignKey("seats.id")),
    db.Column("id_showtime", db.Integer, db.ForeignKey("showtimes.id")),
)


class Cinema(Base):
    __tablename__ = "cinemas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"), unique=True)

    name = db.Column(db.String(100), nullable=False, unique=True)
    rate = db.Column(db.Integer, nullable=False, default=0)

    admin = relationship("Admin", back_populates="cinema")
    films = relationship("Film", secondary=cinema_film, back_populates="cinema")
    showtime_list = relationship(
        "ShowTime", secondary=cinema_showtime, back_populates="cinema_list"
    )

    def __init__(
        self,
        name,
        rate,
        admin_id=None,
    ):
        self.admin_id = admin_id
        self.name = name
        self.rate = rate


class Film(Base):
    __tablename__ = "films"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(100), nullable=False, unique=True)
    rate = db.Column(db.Integer, nullable=False, default=0)

    cinema = relationship("Cinema", secondary=cinema_film, back_populates="films")

    def __init__(self, name):
        self.name = name


class ShowTime(Base):
    __tablename__ = "showtimes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    time = db.Column(db.DATETIME, nullable=False)

    cinema_list = relationship(
        "Cinema", secondary=cinema_showtime, back_populates="showtime_list"
    )
    # seat_list = relationship("Seat", secondary=seat_showtime, back_populates="showtime_list")

    def __init__(self, time, cinema=None):
        self.time = time
        self.cinema_list.append(cinema)


class Seat(Base):
    __tablename__ = "seats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # showtime = relationship("ShowTime", back_populates="seat_list")
    showtime = relationship("ShowTime")
    ticket = relationship("Ticket", back_populates="seat")

    def __init__(self, cinema=None):
        self.showtime_list.append(cinema)


class Ticket(Base):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    seat_id = db.Column(db.Integer, db.ForeignKey("seats.id"), unique=True)
    
    price = db.Column(db.FLOAT)
    
    # user = relationship("User", back_populates="ticket_list")
    user = relationship("User")
    seat = relationship("Seat", back_populates="ticket")

    def __init__(self, user, seat):
        self.user = user
        self.seat = seat
