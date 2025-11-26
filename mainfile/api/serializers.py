from rest_framework import serializers

from myapp.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'in_stock']

    def validate_price(self, attrs):
        if attrs <= 0:
            raise serializers.ValidationError("Price")
        return attrs