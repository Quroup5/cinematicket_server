from config.settings import *

cinema_film = db.Table(
    "cinema_film",
    Base.metadata,
    db.Column("id_cinema", db.Integer, db.ForeignKey("cinemas.id")),
    db.Column("id_film", db.Integer, db.ForeignKey("films.id")),
)

cinema_showtime = db.Table(  # [ ]: It can be cinema_film_showtime
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
    name = db.Column(db.String(100), nullable=False, unique=True)
    rate = db.Column(db.Integer, nullable=False, default=0)
    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"), unique=True)
    admin = relationship("admins", back_populates="cinema")
    films = relationship("films", secondary=cinema_film, back_populates="cinema")

    def __init__(self, name, admin):    # [ ]: What is the usage of __init__() in classes that extends Base?
        self.name = name
        self.admin = admin

    def __str__(self):
        return f" id:{self.id}, name: {self.name}, rate: {self.rate}"


class Film(Base):
    __tablename__ = "films"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    rate = db.Column(db.Integer, nullable=False, default=0)
    cinemas = relationship("cinemas", secondary=cinema_film, back_populates="films")

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f" id:{self.id}, name: {self.name}, rate: {self.rate}"


class ShowTime(Base):
    __tablename__ = "showtimes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DATETIME, nullable=False)


class Seat(Base):
    __tablename__ = "seats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Ticket(Base):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.FLOAT)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    user = relationship("users", back_populates="tickets")

    def __init__(self, user):
        self.user = user
