from django.http import HttpResponse
from http import HTTPStatus


def healthcheck(request):
    return HttpResponse("Health check request has been performed with success",
                        status=HTTPStatus.OK)
