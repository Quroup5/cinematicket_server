import sqlalchemy as db
from sqlalchemy.orm import relationship
from datetime import datetime
from config.settings import Base


class Human:
    def __init__(self, name):
        self.name = name


class Admin(Base, Human):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    # cinema = relationship("Cinema", back_populates="admin")

    def __init__(self, name, password):
        self.name = name
        self.password = password

    # [ ]: implement the create_sans()


class User(Base, Human):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.DATE, nullable=False)
    phone_number = db.Column(db.String(100), nullable=True)
    creation_date = db.Column(db.DATE, nullable=False)
    wallet = db.Column(db.FLOAT, default=0)
    # tickets = relationship("Ticket", back_populates="user")
    # [ ]: write other columns: level

    def __init__(
        self,
        name,
        password,
        email,
        birth_date,
        phone_number,
    ):
        self.name = name
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        self.creation_date = datetime.now()
        self.wallet = 0.0

    def __str__(self):
        return f"{self.name} -- {self.email}"

    # [ ]: implement methods: reserve(), cancel_reserve(), deposit() ...
