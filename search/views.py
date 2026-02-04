from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from products.models import Product
from stores.models import Inventory


class ProductSearchView(APIView):

    def get(self, request):
        query = request.GET.get('q', '').strip()
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        store_id = request.GET.get('store_id')
        in_stock = request.GET.get('in_stock')
        sort = request.GET.get('sort')

        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

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

        if sort == 'price':
            products = products.order_by('price')
        elif sort == 'newest':
            products = products.order_by('-id')

        total_results = products.count()
        start = (page - 1) * page_size
        end = start + page_size
        products = products[start:end]

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

        return Response({
            "page": page,
            "page_size": page_size,
            "total_results": total_results,
            "results": data
        })


class ProductSuggestView(APIView):

    RATE_LIMIT = 20
    WINDOW = 60

    def get(self, request):
        q = request.GET.get('q', '').strip()

        if len(q) < 3:
            return Response(
                {"error": "Minimum 3 characters required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ip = request.META.get('REMOTE_ADDR', 'anonymous')
        cache_key = f"autocomplete_rate:{ip}"

        try:
            count = cache.incr(cache_key)
        except ValueError:
            cache.set(cache_key, 1, timeout=self.WINDOW)
            count = 1

        if count > self.RATE_LIMIT:
            return Response(
                {"error": "Rate limit exceeded"},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        prefix_matches = Product.objects.filter(
            title__istartswith=q
        ).values_list('title', flat=True)[:10]

        remaining_needed = 10 - len(prefix_matches)
        suggestions = list(prefix_matches)

        if remaining_needed > 0:
            other_matches = Product.objects.filter(
                title__icontains=q
            ).exclude(title__istartswith=q)[:remaining_needed]

            suggestions.extend(list(other_matches.values_list('title', flat=True)))

        return Response(suggestions)
