from webob import Response
from config.settings import SessionLocal

from user.models import User, Admin


def signup_user(request):
    response = Response()
    data = request.json
    new_user = User(
        data["name"],
        data["password"],
        data["email"],
        data["year"],
        data["month"],
        data["day"],
        phone_number=data["phone_number"],
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


def login_admin(request):
    response = Response()
    data = request.json
    session = SessionLocal()
    try:
        results = session.query(Admin).filter(Admin.name == data["name"], Admin.password == data["password"]).first()
        results = (
            session.query(Admin)
            .filter(Admin.name == data["name"], Admin.password == data["password"])
            .all()
        )
        if len(results) != 0:
            response.status_code = 200
            response.text = (
                f'welcome {data["name"]}. Your profile info is: \n' + results[0].__str__()
            )
            return response
        else:
            response.status_code = 404
            response.text = f'No such a username: {data["name"]}'
            return response
    finally:
        session.close()