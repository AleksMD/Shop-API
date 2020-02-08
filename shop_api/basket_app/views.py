import json
from decimal import Decimal
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import HttpResponse
from http import HTTPStatus
from basket_app.models import Basket
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Sum
from product_app.models import Product
from shop_api.utils import DecimalJSONEncoder


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


@login_required
@permission_required(('basket_app.view_basket',))
def view_active_basket(request):
    """Returns user's basket with products that have not been paid yet.

    """
    active_basket = request.user.basket_set.filter(active=True).first()
    if not active_basket or len(active_basket.product_set.all()) == 0:
        return HttpResponse('Your basket is empty',
                            status=HTTPStatus.NOT_FOUND)
    response = serializers.serialize('json',
                                     active_basket.product_set.all(),
                                     use_natural_foreign_keys=True)
    return HttpResponse(response,
                        status=HTTPStatus.OK,
                        content_type='application/json')


@login_required
@permission_required(('basket_app.view_basket',))
def view_total_basket_price(request):
    """Returns user's basket with products that have not been paid yet.

    """
    discount = request.user.discount.discount_percent
    active_basket = request.user.basket_set.filter(active=True).first()
    if not active_basket or len(active_basket.product_set.all()) == 0:
        return HttpResponse('Your basket is empty',
                            status=HTTPStatus.NOT_FOUND)
    product_list = serializers.serialize('json',
                                         active_basket.product_set.all(),
                                         fields=['name', 'price'],
                                         use_natural_foreign_keys=True)
    # Following code block calculates total cost(total - total * percent)
    # according to the user discount, if any(default=0).
    # Than serialize it to JSON.
    total_cost = json.dumps(active_basket.product_set.aggregate(
                            total=(Sum('price') - Sum('price') * discount)),
                            cls=DecimalJSONEncoder)
    response = {'product_list': product_list,
                'total_cost': total_cost}
    return HttpResponse(json.dumps(response),
                        status=HTTPStatus.OK,
                        content_type='application/json')


@login_required
@permission_required(('basket_app.change_basket',))
@require_http_methods(['POST'])
def user_payment_view(request):
    """ This view just an emulation of real payment process.
    It receives amount of money in JSON format: {"money": <amount_of_money>}
    if money == total cost it returns OK
    if money < total cost it returns BAD_REQUEST
    """
    discount = request.user.discount.discount_percent
    active_basket = request.user.basket_set.filter(active=True).first()
    money = json.loads(str(request.body, encoding='utf-8'))['money']
    total_cost = active_basket.product_set.aggregate(
                             total=(Sum('price') - Sum('price') * discount))
    if Decimal(str(money)) == total_cost['total']:
        message = 'Transaction was successfull'
        active_basket.active = False
        active_basket.save()
        return HttpResponse(message, status=HTTPStatus.OK)
    elif Decimal(str(money)) < total_cost['total']:
        message = 'The sum of money you have sent is not enough'
        return HttpResponse(message, status=HTTPStatus.BAD_REQUEST)
    else:
        result = Decimal(str(money)) - total_cost['total']
        result = result.quantize(Decimal('1.00'))
        message = (f"You still have some money: {result}!"
                   f" Would you like to buy something else?")
        return HttpResponse(message, status=HTTPStatus.OK)
