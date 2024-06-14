from webob import Response
import json, hashlib

from config.settings import SessionLocal

from user.models import User, Admin
from cinema.models import Cinema, Film


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
        data["rate"],
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


def buy_ticket(request):
    response = Response()
    data = request.json
    session = SessionLocal()
    pass
