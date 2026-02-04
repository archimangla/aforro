from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from products.models import Product


class ProductSuggestView(APIView):

    RATE_LIMIT = 20   # requests
    WINDOW = 60       # seconds

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
            # atomic increment (Redis)
            count = cache.incr(cache_key)
        except ValueError:
            # key does not exist yet
            cache.set(cache_key, 1, timeout=self.WINDOW)
            count = 1

        if count > self.RATE_LIMIT:
            return Response(
                {"error": "Rate limit exceeded"},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # ---- autocomplete logic ----

        prefix_matches = Product.objects.filter(
            title__istartswith=q
        ).values_list('title', flat=True)[:10]

        remaining_needed = 10 - len(prefix_matches)
        suggestions = list(prefix_matches)

        if remaining_needed > 0:
            other_matches = Product.objects.filter(
                title__icontains=q
            ).exclude(
                title__istartswith=q
            ).values_list('title', flat=True)[:remaining_needed]

            suggestions.extend(list(other_matches))

        return Response(suggestions)
