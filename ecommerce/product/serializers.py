from rest_framework import serializers

from ecommerce.product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        ordering = ['created']
        fields = ['id', 'name', 'slug', 'parent']
        extra_kwargs = {'id': {'read_only': True}, 'slug': {'read_only': True}}


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        ordering = ['created']
        fields = [
            'id', 'category', 'name', 'slug', 'description', 'value', 'stock',
            'image'
        ]
        extra_kwargs = {'id': {'read_only': True}, 'slug': {'read_only': True}}
