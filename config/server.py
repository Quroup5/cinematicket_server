from webob import Request, Response
from parse import parse


class API:
    def __init__(self):
        self.routes = {}
        self.default_reponse = Response(status=404, text="Not Found")

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        handler, kwargs = self.find_handler(request_path=request.path)
        if handler is not None:
            return handler(request, **kwargs)
        else:
            return self.default_reponse

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None
