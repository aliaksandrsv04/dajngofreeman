from http.client import HTTPResponse
from pprint import pprint

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from myapp.models import Product
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from unicodedata import category

from .serializers import ProductSerializer


# Create your views here.

@api_view(['GET'])
def test_api(request):
    product = Product.objects.all()
    category = request.query_params.get('category')
    if category:
        product = product.filter(category_id = category)
    return Response([{'id':prod.id,
                     'name':prod.name,
                     'price':prod.price} for prod in product])


class ProductDetailAPIView(APIView):
    def get(self, request):
       products = Product.objects.all()
       serializer = ProductSerializer(products, many = True)
       return Response(serializer.data)

class ProductCreateAPIView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = HTTP_201_CREATED)
        pprint(serializer.errors)
        return Response(serializer.errors,status = HTTP_400_BAD_REQUEST )

@api_view(['GET'])
def set_cookie_example(request):
    response = Response({"message":'Cookie uploaded'})
    response.set_cookie(
        key = '123',
        value = 'abc',
        max_age = 30,
        httponly = True
    )
    return response

@api_view(['GET'])
def get_cookie_example(request):
    tok = request.COOKIES.get('123')
    if tok:
        return Response({"message" : "OK", "token" : tok})
    return Response({"message" : "NO"})
