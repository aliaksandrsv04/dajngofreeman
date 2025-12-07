from rest_framework import serializers

from myapp.models import Product

from myapp.models import CustomUser


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'in_stock']

    def validate_price(self, attrs):
        if attrs <= 0:
            raise serializers.ValidationError("Price")
        return attrs

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email', 'phone')

    def create(self, validated_data):
        user = CustomUser(
            username = validated_data['username'],
            email = validated_data.get('email', ''),
            phone = 'phone'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user