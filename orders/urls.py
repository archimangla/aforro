from django.urls import path
from .views import OrderCreateView, StoreOrderListView

urlpatterns = [
    path('orders/', OrderCreateView.as_view(), name='create-order'),
    path('stores/<int:store_id>/orders/', StoreOrderListView.as_view(), name='store-orders'),
]

