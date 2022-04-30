import logging

logging.basicConfig(level=logging.INFO, filename='sample.log')
from user.models import LogTable


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Welcome to FundoNotes Application")

        response = self.get_response(request)
        log = LogTable(type_of_request=request.method, response=request.get_full_path())
        log.save()

        return response
