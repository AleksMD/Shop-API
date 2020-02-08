import json
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import HttpResponse
from http import HTTPStatus
from product_app.models import Product
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q


@require_http_methods(['GET'])
def get_list_of_all_products(request):
    """Returns list of all products"""

    products = Product.objects.all()
    data_to_return = serializers.serialize('json',
                                           products,
                                           fields=['name', 'price',
                                                   'description', 'category',
                                                   'shop', 'available'],
                                           indent=2,
                                           use_natural_foreign_keys=True)
    return HttpResponse(data_to_return,
                        status=HTTPStatus.OK, content_type='application/json')


@require_http_methods(['GET'])
def get_particular_product(request, pk=None):
    """Returns particular product with details

    Takes a primary key (pk) as a second parameter.
    If product was not found 404 status is returned

    """
    product = Product.objects.filter(pk=pk)
    if product:
        data_to_return = serializers.serialize('json',
                                               product,
                                               fields=['name', 'price',
                                                       'description',
                                                       'category',
                                                       'shop', 'available'],
                                               indent=2,
                                               use_natural_foreign_keys=True)
        return HttpResponse(data_to_return,
                            status=HTTPStatus.OK,
                            content_type='application/json')

    return HttpResponse(status=HTTPStatus.NOT_FOUND)


@login_required
@permission_required(['product_app.add_product'])
@require_http_methods(['POST'])
def create_new_product_in_db(request):
    """Creates a new product in database.
    Require admin's permission.
    Returns custom message and 201 status
    """
    data = json.loads(request.body.decode(encoding='utf-8'))
    Product.objects.create(**data)
    content = (f"Product: name={data['name']}, "
               f"price={data['price']} was created.")
    return HttpResponse(content, status=HTTPStatus.CREATED)


@login_required
@permission_required(['product_app.change_product'])
@require_http_methods(['PUT', 'PATCH'])
def update_existing_product(request, pk=None):
    """ Updates information about existing product
    Require admin's permissions.
    Takes a primary key (pk) as a second parameter.

   The are three possible output:
       if fields are absent in product model - custom message and 400 status

       if product was not found via primary key - custom message and 404 status

       if product was successfully updated - custom message and 204 status
    """
    data = json.loads(request.body.decode(encoding='utf-8'))
    product = Product.objects.filter(pk=pk).first()
    if product:
        try:

            for k, v in data.items():
                if hasattr(product, k):
                    setattr(product, k, v)
                else:
                    raise AttributeError('Wrong field name')
        except AttributeError:
            return HttpResponse('You tried update fields that do not exist!',
                                status=HTTPStatus.BAD_REQUEST)
        else:
            product.save()
            content = f"Product: name={product.name} updated"
            return HttpResponse(content, status=HTTPStatus.NO_CONTENT)
    return HttpResponse(status=HTTPStatus.NOT_FOUND)


@login_required
@permission_required(['product_app.delete_product'])
@require_http_methods(['DELETE'])
def delete_product_from_db(request, pk=None):
    """ Delete existing product from db.
    Require admin's permissions.
    Takes a primary key (pk) as a second parameter.

    The are three possible output.

       - if product was not found via primary key - custom message
       and 400 status

       - if product was successfully updated - custom message
      and 204 status."""

    try:
        product = Product.objects.get(pk=pk)
        product.delete()
    except ObjectDoesNotExist:
        return HttpResponse("You can't delete not existing product",
                            status=HTTPStatus.BAD_REQUEST)
    return HttpResponse("Product was successfully deleted",
                        status=HTTPStatus.NO_CONTENT)


def exact_search_for_product(request):
    """Look through database precisely by using specific filters.

    Function receives json from request get method in a look like:
        {"fieldname": "value"},
        than it is being converted to a dict and forwarding for further
        model querying.
    if either filter name or filter value not correct or absent
    it returns BAD_REQUEST or NOT_FOUND

    """
    data = request.GET.dict()
    try:
        products = Product.objects.filter(**data).all()
    except ValidationError:
        return HttpResponse('Wrong fields values.',
                            status=HTTPStatus.BAD_REQUEST)
    if len(products) > 0:
        data_to_return = serializers.serialize('json',
                                               products,
                                               fields=['name', 'price',
                                                       'description',
                                                       'category',
                                                       'shop', 'available'],
                                               indent=2,
                                               use_natural_foreign_keys=True)
        return HttpResponse(data_to_return,
                            status=HTTPStatus.OK,
                            content_type='application/json')
    return HttpResponse('Nothing was found', status=HTTPStatus.NOT_FOUND)


def approximate_product_search(request):
    """This view allows to search by part of filter value.
    For instance:
        if client requests for {"name": "car"} it returns all db items
        that contains this part of word (carrot, car, cartoon etc.)
    """
    data = request.GET.dict()
    # adding __icontains is equal caseinsensitive SQL method LIKE
    data = {k + '__icontains': v for k, v in data.items()}
    products = Product.objects.filter(**data).all()
    if len(products) > 0:
        data_to_return = serializers.serialize('json',
                                               products,
                                               fields=['name', 'price',
                                                       'description',
                                                       'category',
                                                       'shop', 'available'],
                                               indent=2,
                                               use_natural_foreign_keys=True)
        return HttpResponse(data_to_return,
                            status=HTTPStatus.OK,
                            content_type='application/json')
    return HttpResponse('Nothing was found', status=HTTPStatus.NOT_FOUND)


def product_search_by_shop(request):
    """
    Implements the same functionality as "approximate_product_search".
    the main difference between this and mentioned above is a way of modifying
    filtername due to shop is relational object to product.
    """
    data = request.GET.dict()
    data = {'shop__' + k + '__icontains': v for k, v in data.items()}
    products = Product.objects.filter(**data).all()
    if len(products) > 0:
        data_to_return = serializers.serialize('json',
                                               products,
                                               fields=['name', 'price',
                                                       'description',
                                                       'category',
                                                       'shop', 'available'],
                                               indent=2,
                                               use_natural_foreign_keys=True)
        return HttpResponse(data_to_return,
                            status=HTTPStatus.OK,
                            content_type='application/json')
    return HttpResponse('Nothing was found', status=HTTPStatus.NOT_FOUND)


def product_search_by_price_range(request):
    """ Allows users to search product by price range.
    Recive json in a look like {"from": <start_price>, "to": <end_price>}

    As far as this approach requires more complicated SQL query, method Q was
    imported and implemented. Method Q allows to use AND and OR statement in
    djanto ORM queries.

    """
    data = request.GET.dict()
    start_from = data.get('from', 0)
    end_to = data.get('to', None)
    try:
        products = Product.objects.filter(
            Q(price__gte=start_from) & Q(price__lte=end_to)
            ).all().order_by('price')
    except ValidationError:
        return HttpResponse('Only digits are acceptable',
                            status=HTTPStatus.BAD_REQUEST)
    if len(products) > 0:
        data_to_return = serializers.serialize('json',
                                               products,
                                               fields=['name', 'price',
                                                       'description',
                                                       'category',
                                                       'shop', 'available'],
                                               indent=2,
                                               use_natural_foreign_keys=True)
        return HttpResponse(data_to_return,
                            status=HTTPStatus.OK,
                            content_type='application/json')
    return HttpResponse('Nothing was found', status=HTTPStatus.NOT_FOUND)
