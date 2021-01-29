from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from ecommerce.accounts.models import User
from ecommerce.accounts.serizalizers import (
    UpdateUserSerializer, UserSerializer, PASS_DIDNT_MATCH
)
from ecommerce.accounts.views import UserViewSet

factory = APIRequestFactory()


class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='teste')
        self.user.set_password('#pass123')
        self.user.is_superuser = True
        self.user.save()

    def test_create_ok(self):
        data = {
            'username': 'teste_02', 'password1': '#pass123',
            'password2': '#pass123'
        }
        request = factory.post('api/v1/accounts/', data)
        view = UserViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_pass_not_equals(self):
        data = {
            'username': 'teste_02', 'password1': '#pass123',
            'password2': '#pass1234'
        }
        request = factory.post('api/v1/accounts/', data)
        view = UserViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(str(response.data[0]), PASS_DIDNT_MATCH)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all(self):
        request = factory.get('api/v1/accounts/')
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'get': 'list'})
        response = view(request)
        users = User.objects.filter(id=self.user.id).order_by('created')
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        request = factory.get('api/v1/accounts/',)
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.user.id)
        user = User.objects.get(pk=self.user.id)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {'username': 'teste_02'}
        request = factory.post('api/v1/accounts/', data)
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.user.id)
        user = User.objects.get(pk=self.user.id)
        serializer = UpdateUserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        request = factory.delete('api/accounts/')
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
