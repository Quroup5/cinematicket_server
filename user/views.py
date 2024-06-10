from webob import Response

# from config.url_manager import UrlManager
from config.wsgi import api
from config.settings import session

from user.models import User, Admin

# test_url = UrlManager()

@api.route("/signup")
def sign_up_user(request):
    response = Response()
    # data = request.json
    # new_user = User(
    #     data["name"],
    #     data["password"],
    #     data["email"],
    #     data["year"],
    #     data["month"],
    #     data["day"],
    #     phone_number=data["phone_number"],
    # )
    # try:
    #     session.add(new_user)
    #     session.commit()
    #     response.status_code = 201
    # except:
    #     response.status_code = 405
    
    response.text = "HELLO FROM /signup/"
    response.status_code = 200
    return response
    
        
    

# @api.route("/login/admin")
# def login_admin(request):
#     response = Response()
#     data = request.json
#     admin = Admin(
#         data["name"],
#         data["password"],
#     )
