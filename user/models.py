import sqlalchemy as db
from datetime import datetime, date
from config.settings import Base

class Human:
    def __init__(self, name):
        self.name = name


class Admin(Base, Human):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    # cinema = relationship("Cinema", back_populates="admin", uselist=False) 

    def __init__(self, name, password, Cinema=None):
        self.name = name
        self.password = password
        # self.cinema = Cinema

    def __str__(self):
        return f" id:{self.id}, name: {self.name}"
    
    # [ ]: implement the create_sans()


class User(Base, Human):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=True)
    birth_date = db.Column(db.DATE, nullable=False)
    creation_date = db.Column(db.DATE, nullable=False)
    wallet = db.Column(db.FLOAT, default=0)
    # tickets = relationship("Ticket", back_populates="user")
    # [ ]: write other columns: level

    def __init__(
        self,
        name,
        password,
        email,
        birth_year,
        birth_month,
        birth_day,
        phone_number=None,
    ):
        # self.userid = userid
        self.name = name
        self.password = password
        self.phone_number = phone_number
        self.email = email
        self.birth_date = date(int(birth_year), int(birth_month), int(birth_day))
        self.wallet = 0.0
        self.creation_date = datetime.now()

    def __str__(self):
        return f"id:{self.id}, name: {self.name}, email: {self.email}, phone number: {self.phone_number}, birth date: {self.birth_date}, register date: {self.creation_date}, wallet: {self.wallet} "
    
    # [ ]: implement methods: reserve(), cancel_reserve(), deposit() ...
