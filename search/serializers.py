from rest_framework import serializers

class ProductSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.CharField()
    quantity = serializers.IntegerField(required=False)
