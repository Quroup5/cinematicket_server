from webob import Request, Response
from parse import parse


class API:
    def __init__(self):
        self.routes = {}  # Initialize an empty dictionary to store routes and their corresponding handlers.

    def __call__(self, environ, start_response):
        # The __call__ method allows the instance to be called as a function.
        request = Request(environ)  # Create a Request object from the WSGI environ dictionary.
        response = self.handle_request(request)  # Handle the request and get the response.
        return response(environ, start_response)  # Return the response by calling it with environ and start_response.

    def handle_request(self, request):
        # This method processes the incoming request and generates a response.
        # Create a new Response object.
        handler, kwargs = self.find_handler(request_path=request.path)
        # Find the appropriate handler for the request path.
        if handler is not None:
            # Call the handler with request, response, and any extracted parameters.
            return handler(request, **kwargs)
        else:
            return Response(status=404, text="Not Found")

    def route(self, path):
        # This method is a decorator used to register routes and their handlers.
        def wrapper(handler):
            self.routes[path] = handler  # Add the handler to the routes dictionary with the path as the key.
            return handler

        return wrapper

    def find_handler(self, request_path):
        # This method finds the handler for a given request path.

        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None  # Return the handler if the path matches exactly.
