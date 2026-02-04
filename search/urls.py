from django.urls import path
from .views import ProductSearchView, ProductSuggestView

urlpatterns = [
    path('api/search/products/', ProductSearchView.as_view()),
    path('api/search/suggest/', ProductSuggestView.as_view()),
]
