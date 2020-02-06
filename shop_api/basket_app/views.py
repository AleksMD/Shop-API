import json
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import HttpResponse
from http import HTTPStatus
from basket_app.models import Basket
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from product_app.models import Product


@login_required
@permission_required(('basket_app.view_basket',), raise_exception=True)
@require_http_methods(['GET'])
def get_list_of_all_user_baskets(request):
    """Returns list of all products from basket of particular user."""
    user = request.user
    baskets = Basket.objects.filter(user__pk=user).all()
    data_to_return = serializers.serialize('json', baskets)
    return HttpResponse(data_to_return,
                        status=HTTPStatus.OK, content_type='application/json')


@login_required
@permission_required(('basket_app.change_basket',), raise_exception=True)
@require_http_methods(['GET'])
def add_product_to_basket(request, prod_pk=None):
    """ Retrieve product from database via primary key.
    Get user from request.user and add product to user.basket_set.

    This view requires login and permissions for changing basket
    """
    active_basket = request.user.basket_set.filter(active=True).first()
    if not active_basket:
        active_basket = Basket.objects.create(owner=request.user)
    product_to_add = Product.objects.filter(id=prod_pk,
                                            available=True).first()
    if product_to_add:
        active_basket.product_set.add(product_to_add)
        response = serializers.serialize('json',
                                         active_basket.product_set.all(),
                                         use_natural_foreign_keys=True)

        return HttpResponse(response,
                            status=HTTPStatus.OK,
                            content_type='application/json')
    return HttpResponse('Product you are looking for is absent at the moment',
                        status=HTTPStatus.NOT_FOUND)
