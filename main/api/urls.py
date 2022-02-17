from django.urls import path
from main.api.views import ProductView, ProductImageView


urlpatterns = [
    path('<int:sku>/', ProductView.as_view()),
    path('', ProductView.as_view()),
    path('<int:sku>/image/', ProductImageView.as_view())
]