from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from ecommerce.accounts.models import User
from ecommerce.product.models import Category, Product
from ecommerce.product.serializers import (
    CategorySerializer, ProductSerializer
)
from ecommerce.product.views import (
    CategoryViewSet, ProductViewSet, AddStockView, remove_stock,
    NOT_FOUND_MESSAGE, INSUFICIENT_QUANTITY_MESSAGE
)

factory = APIRequestFactory()


class CategoryViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='teste')
        self.user.set_password('#pass123')
        self.user.is_superuser = True
        self.user.save()

        self.category = Category.objects.create(name='Teste')
        self.category.save()

    def test_create(self):
        data = {'name': 'teste 02'}
        request = factory.post('api/v1/category/', data)
        force_authenticate(request, user=self.user)
        view = CategoryViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all(self):
        request = factory.get('api/v1/category/')
        force_authenticate(request, user=self.user)
        view = CategoryViewSet.as_view({'get': 'list'})
        response = view(request)
        categories = Category.objects.filter(id=self.category.id)
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category(self):
        request = factory.get('api/v1/category/',)
        force_authenticate(request, user=self.user)
        view = CategoryViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.category.id)
        category = Category.objects.get(pk=self.category.id)
        serializer = CategorySerializer(category)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {'name': 'teste 02'}
        request = factory.post('api/v1/category/', data)
        force_authenticate(request, user=self.user)
        view = CategoryViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.category.id)
        category = Category.objects.get(pk=self.category.id)
        serializer = CategorySerializer(category)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        request = factory.delete('api/category/')
        force_authenticate(request, user=self.user)
        view = CategoryViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.category.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='teste')
        self.user.set_password('#pass123')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.category = Category.objects.create(name='Teste Cat')
        self.category.save()

        self.product = Product.objects.create(
            category=self.category, name='Produto Teste',
            description='Lorem ipsum', value=15.5, stock=10
        )
        self.product.save()

    def test_create(self):
        data = {
            'category': self.category.id, 'name': 'Produto Teste 2',
            'description': 'Lorem ipsum', 'value': 15.5, 'stock': 10
        }
        request = factory.post('api/v1/product/', data)
        force_authenticate(request, user=self.user)
        view = ProductViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all(self):
        request = factory.get('api/v1/product/')
        force_authenticate(request, user=self.user)
        view = ProductViewSet.as_view({'get': 'list'})
        response = view(request)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product(self):
        request = factory.get('api/v1/product/',)
        force_authenticate(request, user=self.user)
        view = ProductViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.product.id)
        product = Product.objects.get(pk=self.product.id)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {
            'category': self.category.id, 'name': 'Produto Teste 2',
            'description': 'Lorem ipsum', 'value': 15.5, 'stock': 10
        }
        request = factory.post('api/v1/product/', data)
        force_authenticate(request, user=self.user)
        view = ProductViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.product.id)
        product = Product.objects.get(pk=self.product.id)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_stock_ok(self):
        data = {'product': self.product.pk, 'quantity': 25}
        request = factory.post('api/v1/product/add_stock', data)
        force_authenticate(request, user=self.user)
        view = AddStockView.as_view()
        response = view(request)
        product = Product.objects.get(pk=self.product.id)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_stock_fail(self):
        data = {'product': str(self.product.pk) + 'a', 'quantity': 25}
        request = factory.post('api/v1/product/add_stock', data)
        force_authenticate(request, user=self.user)
        view = AddStockView.as_view()
        response = view(request)
        self.assertEqual(response.data, {NOT_FOUND_MESSAGE})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_stock_ok(self):
        data = {'product': self.product.pk, 'quantity': 1}
        request = factory.post('api/v1/product/remove_stock', data)
        force_authenticate(request, user=self.user)
        response = remove_stock(request)
        product = Product.objects.get(pk=self.product.id)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_stock_not_found(self):
        data = {'product': str(self.product.pk) + 'a', 'quantity': 5}
        request = factory.post('api/v1/product/remove_stock', data)
        force_authenticate(request, user=self.user)
        response = remove_stock(request)
        self.assertEqual(response.data, {NOT_FOUND_MESSAGE})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_stock_most_quantity(self):
        data = {'product': self.product.pk, 'quantity': 1000}
        request = factory.post('api/v1/product/remove_stock', data)
        force_authenticate(request, user=self.user)
        response = remove_stock(request)
        self.assertEqual(response.data, {INSUFICIENT_QUANTITY_MESSAGE})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        request = factory.delete('api/product/')
        force_authenticate(request, user=self.user)
        view = ProductViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
