from django.urls import path, include

from rest_framework import routers

from ecommerce.accounts import views

app_name = 'accounts'

router = routers.DefaultRouter()

router.register('', views.UserViewSet, basename='accounts')

urlpatterns = [path('', include(router.urls))]
