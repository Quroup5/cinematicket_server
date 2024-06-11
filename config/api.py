from webob import Response

from config.server import API
from config.settings import engine, Base
import user.views as uv

api = API()
Base.metadata.create_all(bind=engine)

@api.route("/signup/user/")
def signup_user(request):
    try:
        return uv.signup_user(request)
    except:
        response = Response(status=400)
        response.text = "BAD REQUEST!"
        return response

@api.route("/login/admin/")
def login_admin(request):
    try:
        return uv.login_admin(request)
    except Exception as e:
        print(e)
        response = Response(status=400)
        response.text = "BAD REQUEST!"
        return response