from config.settings import Base, engine
from config.settings import SessionLocal
from datetime import datetime
from user.models import User, Admin, BankAccount
from cinema.models import Cinema, Film, ShowTime, Seat, Ticket

Base.metadata.create_all(engine)




def generate_cinema(film=None):

        cinema= Cinema(f"cinema{1}", 0, 1)
        #cinema.films.append(film)
        session = SessionLocal()
        try:
            session.add(cinema)
            session.commit()
            return cinema
        finally:
            session.close()
            return None

def generate_admin():

    admin = Admin(f"admin", '1234')
    session = SessionLocal()
    try:
        session.add(admin)
        session.commit()
        return admin
    finally:
        session.close()
        return None




if __name__ == "__main__":
    pass
    # film1 = Film('Titanic')
    # film2 = Film('E.T.')
    # film3 = Film('Avatar')
    #session= SessionLocal()
    # session.add(film1)
    # session.add(film2)
    # session.add(film3)
    #
    # admin1 = generate_admin()
    # cinema2 = generate_cinema()
    # cinema2 = session.query(Cinema).first()
    # cinema2.films.append(film1)
    #
    # st1 = ShowTime(datetime.now(), cinema2)
    # session.add(st1)
    # session.commit()
    # print(session.query(Cinema).first())
    # st_1 = session.query(ShowTime).first()
    # seat = Seat(st_1)
    #ba1 = BankAccount('RBC', '83838', '344', '12133', session.query(User).first())
    #session.add(seat)
    #
    # t1 = Ticket(session.query(User).first(),session.query(Seat).first())
    # session.add(t1)
    # session.commit()