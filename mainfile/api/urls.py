from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import test_api, ProductDetailAPIView, ProductCreateAPIView, set_cookie_example, get_cookie_example, \
    ProductsAPIView, RegisterAPIView, LogoutAPIView

urlpatterns = [
    path('api1/', test_api, name='test_api'),
    path("products/", ProductsAPIView.as_view(), name = "products_api" ),
    path("products/detail/<int:pk>", ProductDetailAPIView.as_view(), name="products_detail_api"),
    path("products/create", ProductCreateAPIView.as_view(), name = "products_create_api"),



    path("cookie", set_cookie_example, name = "cookies"),
    path("cookie_get", get_cookie_example, name = "cookies_get"),


    path('token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),



    path('register/', RegisterAPIView.as_view(), name = 'api_register'),
    path('logout/', LogoutAPIView.as_view(), name = 'api_logout')
]
# {
#     "username": "alex1",
#     "email" : "12@1.com",
#     "password": "12345678",
#     "phone": "48793512241"
# }