import datetime

from webob import Response
from config.settings import SessionLocal, engine, Base
from cinema.models import Cinema, Film
import os
from user.models import User, Admin, BankAccount
from cinema.models import Cinema, Film, ShowTime, Seat, Ticket


def add_film(admin_id, film_name):
    session = SessionLocal()
    try:
        cinema1 = session.query(Cinema).filter(Cinema.admin_id == admin_id).first()
        film_object = session.query(Film).filter(Film.name == film_name).first()
        print(film_object)
        cinema1.films.append(film_object)
        session.commit()
        #response.status_code = 201
    except:
        pass

    finally:

        session.close()


def add_show_time(admin_id, time, film_name, numbers_seat):
    session = SessionLocal()
    cinema = session.query(Cinema).filter(Cinema.admin_id == admin_id).first()

    list_film_names = list(map(lambda x: x.name, cinema.films))
    #print(list_film_names)
    if film_name not in list_film_names:
        return "This film doesnt exist in cinema"

    show = ShowTime(time, cinema)
    for _ in range(numbers_seat):
        seat = Seat(showtime=show)
        # seat.showtime = show
        ticket = Ticket(seat)
        ticket.price = 20
        session.add(seat)
        session.add(ticket)

    try:
        session.add(show)

        session.commit()

    except:
        pass
    finally:
        session.close()
        return "OK"


def show_tickets(user_id, cinema_name, film_name, time):
    session = SessionLocal()
    cinema = session.query(Cinema).filter(Cinema.name == cinema_name).first()
    showtime = session.query(ShowTime).filter(ShowTime.time == time).first()
    seat_list = session.query(Seat).filter(Seat.showtime_id == showtime.id).all()
    list_film_names = list(map(lambda x: x.name, cinema.films))

    if film_name not in list_film_names:
        return "This film doesnt exist in cinema"

    for number, seat in enumerate(seat_list):
        if number % 5 == 0:
            print()

        ticket = session.query(Ticket).filter(Ticket.seat_id == seat.id).first()
        #print(ticket, seat, number)
        if not ticket.users_id:
            char = number + 1
        else:
            char = '*'
        print(char, end=' ')

    return 'OK'


def buy_ticket(user_id, cinema_name, film_name, time, seat_id):
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    cinema = session.query(Cinema).filter(Cinema.name == cinema_name).first()
    showtime = session.query(ShowTime).filter(ShowTime.time == time).first()
    list_film_names = list(map(lambda x: x.name, cinema.films))

    if film_name not in list_film_names:
        return "This film doesnt exist in cinema"

    ticket = session.query(Ticket).filter(Ticket.seat_id == seat_id).first()
    if ticket.users_id == None:
        if user.wallet - ticket.price >= 0:
            ticket.users_id = user_id
            user.ticket_list.append(ticket)
            user.wallet -= ticket.price
            session.commit()
            print("reserved")
        else:
            return "Insufficient Fund"
    else:
        return "This Seat has been already reserved!"

    return 'OK'

if __name__ == "__main__":
    if not os.path.exists("database.db"):
        Base.metadata.create_all(bind=engine)
        session = SessionLocal()

        admin1 = Admin("admin1", "1234")
        admin2 = Admin("admin2", "1234")

        cinema1 = Cinema('rex', 0)
        cinema2 = Cinema('ABC', 0)

        film1 = Film("UP")
        film2 = Film("Down")

        cinema1.admin = admin1
        cinema2.admin = admin2
        user1 = User('am', '123', 'am@gmail.com', "1990-03-03", '455455444')
        user1.wallet = 40.0

        session.add(admin1)
        session.add(user1)
        session.add(film1)
        session.add(film2)
        session.add(cinema1)

        session.commit()

        add_film(1, "UP")
        date_string = "2024-06-14 20:00"
        date_format = "%Y-%m-%d %H:%M"
        time = datetime.datetime.strptime(date_string, date_format)
        add_show_time(1, time, 'UP', 10)

    date_string = "2024-06-14 20:00"
    date_format = "%Y-%m-%d %H:%M"
    time = datetime.datetime.strptime(date_string, date_format)
    print(buy_ticket(1, 'rex', 'UP', time, 2))
    print(show_tickets(1, 'rex', 'UP', time))
