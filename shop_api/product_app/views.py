import json
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import HttpResponse
from http import HTTPStatus
from product_app.models import Product
from django.core.exceptions import ObjectDoesNotExist


@require_http_methods(['GET'])
def get_list_of_all_products(request):
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
    data = json.loads(request.body.decode(encoding='utf-8'))
    Product.objects.create(**data)
    content = (f"Product: name={data['name']}, "
               f"price={data['price']} was created.")
    return HttpResponse(content, status=HTTPStatus.CREATED)


@login_required
@permission_required(['product_app.change_product'])
@require_http_methods(['PUT'])
def update_existing_product(request, pk=None):
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
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
    except ObjectDoesNotExist:
        return HttpResponse("You can't delete not existing product",
                            status=HTTPStatus.BAD_REQUEST)
    return HttpResponse("Product was successfully deleted",
                        status=HTTPStatus.NO_CONTENT)


def exact_search_for_product(request):
    data = request.GET.dict()
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


def approximate_product_search(request):
    data = request.GET.dict()
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
    ...
