from rest_framework import serializers
from .models import Product, Category, STLModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'tipo']


class STLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = STLModel
        fields = ['file', 'volume_cm3', 'weight_gr']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    stl_model = STLModelSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'base_price',
            'category', 'stock', 'activo', 'stl_model'
        ]
