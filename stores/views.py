from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Inventory
from .serializers import StoreInventorySerializer

class StoreInventoryView(APIView):

    def get(self, request, store_id):
        inventory = (
            Inventory.objects
            .filter(store_id=store_id)
            .select_related('product', 'product__category')
            .order_by('product__title')
        )

        serializer = StoreInventorySerializer(inventory, many=True)
        return Response(serializer.data)
