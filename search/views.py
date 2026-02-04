from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from stores.models import Inventory
from .serializers import ProductSearchSerializer


class ProductSearchView(APIView):

    def get(self, request):
        query = request.GET.get('q', '').strip()
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        store_id = request.GET.get('store_id')
        in_stock = request.GET.get('in_stock')

        products = Product.objects.select_related('category')

        if query:
            products = products.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        if category:
            products = products.filter(category__name__iexact=category)

        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)

        inventory_map = {}

        if store_id:
            inventory_qs = Inventory.objects.filter(
                store_id=store_id,
                product__in=products
            )

            if in_stock == 'true':
                inventory_qs = inventory_qs.filter(quantity__gt=0)

            inventory_map = {
                inv.product_id: inv.quantity
                for inv in inventory_qs
            }

            products = products.filter(id__in=inventory_map.keys())

        data = []
        for p in products:
            item = {
                "id": p.id,
                "title": p.title,
                "price": p.price,
                "category": p.category.name,
            }

            if store_id:
                item["quantity"] = inventory_map.get(p.id, 0)

            data.append(item)

        serializer = ProductSearchSerializer(data, many=True)
        return Response(serializer.data)
