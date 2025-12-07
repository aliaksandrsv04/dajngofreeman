from http.client import HTTPResponse
from pprint import pprint
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from myapp.models import Product
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from unicodedata import category

from .serializers import ProductSerializer, RegisterSerializer
from .permissions import IsManager


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


class ProductsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsManager, IsAuthenticated]
    @method_decorator(cache_page(30))
    def get(self, request):
       products = Product.objects.all()
       serializer = ProductSerializer(products, many = True)
       return Response(serializer.data)


class ProductDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            products = Product.objects.get(pk=pk)
            serializer = ProductSerializer(products)
        except:
            return Response({'error': 'Product not found'}, status=404)

        return Response(serializer.data, status=200)




class ProductCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsManager, IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = 'Create product',
        request_body= ProductSerializer,
        responses={
            201:"Created",
            400:'Bad Request',
            401:'Unauthorized',
            403:'Forbidden'
        },
    )

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



class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'id' : user.id,
                'username' : user.username,
                'email' : user.email,
            }
            return Response(data, status = HTTP_201_CREATED)
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required"}, status= HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            # помечаем refresh в blacklist
            token.blacklist()
            return Response(status= status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Token invalid or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)