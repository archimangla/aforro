from django.urls import path
from .views import ProductSearchView

urlpatterns = [
    path('api/search/products/', ProductSearchView.as_view()),
]
