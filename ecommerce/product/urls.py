from django.urls import path, include

from rest_framework import routers

from ecommerce.product import views

app_name = 'product'

router = routers.DefaultRouter()

router.register('category', views.CategoryViewSet, basename='category')
router.register('product', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('product/add_stock', views.AddStockView.as_view(), name='add_stock'),
    path('product/remove_stock', views.remove_stock, name='remove_stock'),
]
