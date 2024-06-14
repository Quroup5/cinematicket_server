from webob import Response

from config.server import API
from config.settings import engine, Base
import user.views as uv
import cinema.views as cv

api = API()
Base.metadata.create_all(bind=engine)


@api.route("/user/signup/")
def signup_user(request):
    try:
        return uv.signup_user(request)
    except Exception as e:
        print(e)
        response = Response(status=400)
        response.text = "BAD REQUEST!"
        return response


@api.route("/user/login/")
def login_user(request):
    try:
        return uv.login_user(request)
    except Exception as e:
        print(e)
        response = Response(status=400)
        response.text = "BAD REQUEST!"
        return response


@api.route("/user/profile/")
def get_profile(request):
    try:
        return uv.get_profile(request)
    except Exception as e:
        print(e)
        response = Response(status=400)
        response.text = "BAD REQUEST!"
        return response


@api.route("/user/buyticket/")
def buy_ticket(request):
    try:
        return uv.buy_ticket(request)
    except Exception as e:
        print(e)
        response = Response(status=400)
        response.text = "BAD REQUEST!"
        return response


@api.route("/admin/login/")
def login_admin(request):
    try:
        return uv.login_admin(request)
    except Exception as e:
        print(e)
        response = Response(status=400)
        response.text = "BAD REQUEST!"
        return response


@api.route("/admin/addcinema/")
def add_cinema(request):
    try:
        return uv.add_cinema(request)
    except Exception as e:
        print(e)
        response = Response(status=400)
        response.text = "BAD REQUEST!"
        return response





#-----------------------


