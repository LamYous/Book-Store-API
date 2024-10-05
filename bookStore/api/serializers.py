from .models import Book, Category, Order
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class OrderSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

