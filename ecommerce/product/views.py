from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import parsers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from ecommerce.product.models import Category, Product
from ecommerce.product.permissions import IsAdminOrReadOnly
from ecommerce.product.serializers import (
    CategorySerializer, ProductSerializer
)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = (
        'name', 'parent', 'parent__slug', 'parent__name', 'slug'
    )
    search_fields = [
        'name', 'parent__slug', 'parent__name', 'slug'
        ]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering = ('-created')


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = (
        'category', 'category__name', 'category__slug',
        'category__parent__slug', 'category__parent__name', 'name', 'slug',
        'description', 'value', 'stock'
    )
    search_fields = [
        'category__name', 'category__slug', 'category__parent__slug',
        'category__parent__name', 'name', 'slug', 'description', 'value',
        'stock', 'category__parent__parent__slug',
        'category__parent__parent__parent__slug',
    ]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    ordering = ('-created')


NOT_FOUND_MESSAGE = 'Produto não encontrado'


class AddStockView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        try:
            product = Product.objects.get(id=request.data['product'])
            product.stock += int(request.data['quantity'])
            product.save()
            serializer = ProductSerializer(product)
            data = serializer.data
            status_req = status.HTTP_200_OK
        except Exception:
            data = {NOT_FOUND_MESSAGE}
            status_req = status.HTTP_404_NOT_FOUND

        return Response(data, status=status_req)


INSUFICIENT_QUANTITY_MESSAGE = 'Quantidade insuficiente'


@api_view(['POST'])
@permission_classes([IsAdminUser])
def remove_stock(request):
    try:
        product = Product.objects.get(id=request.data['product'])

        data = {INSUFICIENT_QUANTITY_MESSAGE}
        status_req = status.HTTP_400_BAD_REQUEST

        if product.stock >= int(request.data['quantity']):
            product.stock -= int(request.data['quantity'])
            product.save()
            serializer = ProductSerializer(product)
            data = serializer.data
            status_req = status.HTTP_200_OK

    except Exception:
        data = {NOT_FOUND_MESSAGE}
        status_req = status.HTTP_404_NOT_FOUND

    return Response(data, status=status_req)
