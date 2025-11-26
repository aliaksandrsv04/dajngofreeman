from django.urls import path

from .views import test_api, ProductDetailAPIView, ProductCreateAPIView, set_cookie_example, get_cookie_example, \
    ProductsAPIView

urlpatterns = [
    path('api1/', test_api, name='test_api'),
    path("products/", ProductsAPIView.as_view(), name = "products_api" ),
    path("products/detail/<int:pk>", ProductDetailAPIView.as_view(), name="products_detail_api"),
    path("products/create", ProductCreateAPIView.as_view(), name = "products_create_api"),
    path("cookie", set_cookie_example, name = "cookies"),
    path("cookie_get", get_cookie_example, name = "cookies_get")
]