import json
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from http import HTTPStatus
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User, Permission
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login


def healthcheck(request):
    return HttpResponse("Health check request has been performed with success",
                        status=HTTPStatus.OK)


def index(request):
    index_page_emulation = '<h2>Welcome To Shop API</h2>'
    return HttpResponse(index_page_emulation, status=HTTPStatus.OK)


@csrf_exempt
@require_http_methods(['POST'])
def signup_page(request):
    data = json.loads(request.body.decode(encoding='utf-8'))
    try:
        user = User.objects.create_user(**data)

        # Grants permission for user to change and to see basket.
        change_basket_perm = Permission.objects.get(codename='change_basket')
        view_basket_perm = Permission.objects.get(codename='view_basket')
        user.user_permissions.add(view_basket_perm, change_basket_perm)
        user.save()

        message = 'You have been successfully signed up!'
        return HttpResponse(message, status=HTTPStatus.CREATED)
    except ValidationError:
        message = 'You have provided invalid data for sign up.'
        return HttpResponse(message, status=HTTPStatus.BAD_REQUEST)


@csrf_exempt
@require_http_methods(['POST'])
def login_page(request):
    data = json.loads(request.body.decode(encoding='utf-8'))
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        message = 'You have successfully logged in'
        return HttpResponse(message, status=HTTPStatus.OK)
    return HttpResponse('Incorrect login/password!',
                        status=HTTPStatus.BAD_REQUEST)
