from webob import Response
from config.settings import SessionLocal

from cinema.models import Cinema, Film






# test of generating cinema in

def generate_cinema(num):
    for idx in range(num):
        cineam= Cinema(f"name{idx}", password='1234')
        session = SessionLocal()
        try:
            session.add(cineam)
            session.commit()
        finally:
            session.close()