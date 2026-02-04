from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from stores.models import Inventory
from .serializers import ProductSearchSerializer

class ProductSearchView(APIView):

    def get(self, request):
        query = request.GET.get('q', '').strip()

        products = Product.objects.select_related('category')

        if query:
            products = products.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        data = []
        for p in products:
            data.append({
                "id": p.id,
                "title": p.title,
                "price": p.price,
                "category": p.category.name,
            })

        serializer = ProductSearchSerializer(data, many=True)
        return Response(serializer.data)
