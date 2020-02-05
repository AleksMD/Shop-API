from django.http import HttpResponse
from http import HTTPStatus


def healthcheck(request):
    return HttpResponse("Health check request has been performed with success",
                        status=HTTPStatus.OK)


def index(request):
    index_page_emulation = '<h2>Welcome To Shop API</h2>'
    return HttpResponse(index_page_emulation, status=HTTPStatus.OK)
