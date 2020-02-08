import json
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import HttpResponse
from http import HTTPStatus
from shop_app.models import Shop
from django.core.exceptions import ValidationError, ObjectDoesNotExist


@login_required
@permission_required(('shop_app.add_shop',))
@require_http_methods(['POST'])
def add_new_shop_view(request):
    """Creates new shop from received JSON.
    Only admin permissions is allowed.
    """
    shop_data = json.loads(str(request.body, encoding='utf-8'))
    try:
        Shop.objects.create(**shop_data)
    except ValidationError:
        return HttpResponse('Please, check fields you tried to fill in',
                            status=HTTPStatus.BAD_REQUEST)
    message = 'Shop was successfully added'
    return HttpResponse(message, status=HTTPStatus.CREATED)


@login_required
@permission_required(('shop_app.change_shop',))
@require_http_methods(['PUT', 'PATCH'])
def change_existing_shop_view(request, shop_pk=None):
    """Updates shop from with data in received JSON.
    Retrieve shop from db via primary key.
    Only admin permissions is allowed.
    """
    shop_data = json.loads(str(request.body, encoding='utf-8'))
    try:
        shop = Shop.objects.get(id=shop_pk)
        for k, v in shop_data.items():
            if hasattr(shop, k):
                setattr(shop, k, v)
            else:
                raise AttributeError('Wrong field name')
    except ObjectDoesNotExist:
        return HttpResponse('Shop with this id does not exist!',
                            status=HTTPStatus.BAD_REQUEST)
    except AttributeError:
        return HttpResponse('You tried to modify not existing field(s) ',
                            status=HTTPStatus.BAD_REQUEST)
    else:
        shop.save()
    message = 'Shop was successfully modified'
    return HttpResponse(message, status=HTTPStatus.OK)


@require_http_methods(['GET'])
def get_list_of_all_shops(request):
    """Returns list of all shops in JSON."""

    shops = Shop.objects.all()
    data_to_return = serializers.serialize('json',
                                           shops,
                                           fields=['name', 'city', 'owner'],
                                           indent=2,
                                           use_natural_foreign_keys=True)
    return HttpResponse(data_to_return,
                        status=HTTPStatus.OK, content_type='application/json')


@require_http_methods(['GET'])
def get_particular_shop(request, shop_pk=None):
    """Returns particular shop with details in JSON.

    Takes a primary key (pk) as a second parameter.
    If shop was not found 404 status is returned

    """
    shop = Shop.objects.filter(pk=shop_pk)
    if shop:
        data_to_return = serializers.serialize('json',
                                               shop,
                                               indent=2,
                                               use_natural_foreign_keys=True)
        return HttpResponse(data_to_return,
                            status=HTTPStatus.OK,
                            content_type='application/json')

    return HttpResponse(status=HTTPStatus.NOT_FOUND)
