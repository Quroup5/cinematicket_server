class UrlManager:
    def __init__(self) -> None:
        self.routes = dict()
    
    def route(self, path):
        print("Inside ROUTE", path)
        def wrapper(handler):
            print("Inside WRAPPER", handler)
            self.routes[path] = handler
            return handler
        return wrapper
    
    def setup_route(self, wsgi):
        wsgi.routes.update(self.routes)