from webob import Response
import hashlib, datetime

from config.settings import SessionLocal

from user.models import User, Admin
from cinema.models import Cinema, Film, ShowTime, Seat, Ticket


def signup_user(request):
    response = Response()
    data = request.json
    new_user = User(
        data["name"],
        data["password"],
        data["email"],
        data["birth_date"],
        data["phone_number"],
    )

    session = SessionLocal()

    try:
        session.add(new_user)
        session.commit()
        response.status_code = 201
    except:
        response.status_code = 405
    finally:
        session.close()
    return response


def login_user(request):
    response = Response()
    data = request.json
    session = SessionLocal()
    try:
        encoder = hashlib.new("SHA256")
        encoder.update(bytes(data["password"], "utf-8"))

        result = (
            session.query(User)
            .filter(User.name == data["name"], User.password == encoder.hexdigest())
            .first()
        )

        if result:
            response.status_code = 200
            return response
        else:
            response.status_code = 403
            response.text = f'No such a user: {data["name"]}'
            return response
    except Exception as e:
        print(e)
        response.status_code = 405
        return response

    finally:
        session.close()


def get_profile(request):
    response = Response()
    data = request.json
    session = SessionLocal()
    try:
        encoder = hashlib.new("SHA256")
        encoder.update(bytes(data["password"], "utf-8"))

        result = (
            session.query(User)
            .filter(User.name == data["name"], User.password == encoder.hexdigest())
            .first()
        )
        if result:
            response.status_code = 200
            response.content_type = "application/json"
            response.json = {
                "name": result.name,
                "password": result.password,
                "email": result.email,
                "birth_date": result.birth_date.strftime("%Y-%m-%d"),
                "phone_number": result.phone_number,
            }
            return response
        else:
            response.status_code = 404
            response.text = f'No such a user: {data["name"]}'
            return response
    except Exception as e:
        print(e)
        response.status_code = 405
        return response

    finally:
        session.close()


def login_admin(request):
    response = Response()
    data = request.json
    session = SessionLocal()
    try:
        encoder = hashlib.new("SHA256")
        encoder.update(bytes(data["password"], "utf-8"))

        result = (
            session.query(Admin)
            .filter(Admin.name == data["name"], Admin.password == encoder.hexdigest())
            .first()
        )

        if result:
            response.status_code = 200
            return response
        else:
            response.status_code = 403
            response.text = f'No such a admin: {data["name"]}'
            return response
    except Exception as e:
        print(e)
        response.status_code = 405
        return response

    finally:
        session.close()


def signup_admin(request):
    response = Response()
    data = request.json
    new_admin = Admin(
        data["name"],
        data["password"],
    )

    session = SessionLocal()

    try:
        session.add(new_admin)
        session.commit()
        response.status_code = 201
    except:
        response.status_code = 405
    finally:
        session.close()
    return response


def add_cinema(request):
    response = Response()
    data = request.json
    new_cinema = Cinema(
        data["name"],
        data["admin_id"],
    )

    session = SessionLocal()

    try:
        session.add(new_cinema)
        session.commit()
        response.status_code = 201
    except:
        response.status_code = 405
    finally:
        session.close()
    return response


def add_film(request):
    response = Response()
    data = request.json
    new_film = Film(
        data["film_name"],
    )

    session = SessionLocal()

    try:
        target_cinema = (
            session.query(Cinema).filter(Cinema.name == data["cinema_name"]).first()
        )
        new_film.cinema.append(target_cinema)
        session.add(new_film)
        session.commit()
        response.status_code = 201

    except Exception as e:
        print(e)
        response.status_code = 405
        return response

    finally:
        session.close()

    return response


def add_showtime(request):
    response = Response()
    data = request.json
    session = SessionLocal()

    try:
        target_cinema = (
            session.query(Cinema).filter(Cinema.name == data["cinema_name"]).first()
        )

        target_films = target_cinema.films

        list_film_names = list(map(lambda x: x.name, target_films))

        if data["film_name"] not in list_film_names:
            response.status_code = 404
            response.text = f'No such a film: {data["film_name"]}'
            return response

        new_showtime = ShowTime(data["time"], target_cinema)

        for _ in range(36):
            new_seat = Seat(showtime=new_showtime)
            new_ticket = Ticket(new_seat)
            new_ticket.price = data["price"]
            session.add(new_seat)
            session.add(new_ticket)

        session.commit()
        response.status_code = 201

    except Exception as e:
        print(e)
        response.status_code = 405
        return response

    finally:
        session.close()

    return response


def buy_ticket(request):
    response = Response()
    data = request.json
    session = SessionLocal()
    try:
        target_cinema = (
            session.query(Cinema).filter(Cinema.name == data["cinema_name"]).first()
        )
        target_films = target_cinema.films
        list_film_names = list(map(lambda x: x.name, target_films))

        if data["film_name"] not in list_film_names:
            response.status_code = 404
            response.text = f'No such a film: {data["film_name"]}'
            return response

        user = session.query(User).filter(User.id == data["user_id"]).first()
        ticket = session.query(Ticket).filter(Ticket.seat_id == data["seat_id"]).first()

        if ticket.users_id == None:
            if user.wallet - ticket.price >= 0:
                ticket.users_id = data["user_id"]
                user.ticket_list.append(ticket)
                user.wallet -= ticket.price
                session.commit()

                response.status_code = 200
                response.text = "Reserved!"

                session.close()
                return response
            else:
                response.status_code = 201
                response.text = "Insufficient Fund"

                session.close()
                return response
        else:
            response.status_code = 202
            response.text = "This seat has been already reserved!"

            session.close()
            return response

    except Exception as e:
        print(e)
        response.status_code = 405
        return response


def show_tickets(request):
    response = Response()
    data = request.json
    session = SessionLocal()
    try:
        target_cinema = (
            session.query(Cinema).filter(Cinema.name == data["cinema_name"]).first()
        )
        target_films = target_cinema.films
        list_film_names = list(map(lambda x: x.name, target_films))

        if data["film_name"] not in list_film_names:
            response.status_code = 404
            response.text = f'No such a film: {data["film_name"]}'
            return response

        user = session.query(User).filter(User.id == data["user_id"]).first()
        ticket = session.query(Ticket).filter(Ticket.seat_id == data["seat_id"]).first()
        showtime = (
            session.query(ShowTime)
            .filter(ShowTime.time == datetime.strptime(data["time"], "%Y-%m-%d %H:%M"))
            .first()
        )
        seat_list = session.query(Seat).filter(Seat.showtime_id == showtime.id).all()

        tickets = dict()

        for seat in seat_list:
            ticket = session.query(Ticket).filter(Ticket.seat_id == seat.id).first()
            ticket[ticket.id] = {
                "users_id": ticket.users_id,
                "seat_id": ticket.seat_id,
                "price": ticket.price,
            }

        response.status_code = 200
        response.json = tickets

        session.close()
        return response

    except Exception as e:
        print(e)
        response.status_code = 405
        return response
