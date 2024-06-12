from webob import Response
from config.settings import SessionLocal

from cinema.models import Cinema, Film

def add_new_cinema(request):
    response = Response()
    data = request.json
    new_cinema = Cinema(
        data["name"],
        data["rate"],
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

def add_film_to_cinema(request):
    response = Response()
    data = request.json
    new_film = Film(
        data["name"],
        data["rate"],
        data["cinema"],
    )