from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from stores.models import Store, Inventory
from products.models import Product
from .models import Order, OrderItem
from .serializers import OrderCreateSerializer


class OrderCreateView(APIView):

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        store_id = serializer.validated_data['store_id']
        items = serializer.validated_data['items']

        store = get_object_or_404(Store, id=store_id)

        with transaction.atomic():

            order = Order.objects.create(
                store=store,
                status=Order.Status.PENDING
            )

            inventory_map = {}

            inventory_qs = Inventory.objects.select_for_update().filter(
                store=store,
                product_id__in=[item['product_id'] for item in items]
            )

            for inv in inventory_qs:
                inventory_map[inv.product_id] = inv

            insufficient_stock = False

            for item in items:
                product_id = item['product_id']
                qty = item['quantity_requested']

                inventory = inventory_map.get(product_id)

                if not inventory or inventory.quantity < qty:
                    insufficient_stock = True
                    break

            if insufficient_stock:
                order.status = Order.Status.REJECTED
                order.save()

            else:
                for item in items:
                    inventory = inventory_map[item['product_id']]
                    inventory.quantity -= item['quantity_requested']
                    inventory.save()

                    OrderItem.objects.create(
                        order=order,
                        product_id=item['product_id'],
                        quantity_requested=item['quantity_requested']
                    )

                order.status = Order.Status.CONFIRMED
                order.save()

        return Response(
            {
                "order_id": order.id,
                "status": order.status
            },
            status=status.HTTP_201_CREATED
        )
