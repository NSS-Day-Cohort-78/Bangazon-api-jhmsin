from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers
from bangazonapi.models import Store
from rest_framework.response import Response
from .customer import Customer, CustomerUserSerializer, CustomerProductSerializer

# class StoreProductsSerializer(serializers.ModelSerializer):
#     """JSON serializer"""
#     products = CustomerProductSerializer(many=True)

#     class Meta:
#         model = Customer
#         fields


class StoreOwnerSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    user = CustomerUserSerializer(many=False)
    products = CustomerProductSerializer(many=True)

    class Meta:
        model = Customer
        fields = (
            "id",
            "user",
            "products",
        )


class StoreSerializer(serializers.ModelSerializer):
    """JSON serializer for product category"""

    customer = StoreOwnerSerializer(many=False)

    class Meta:
        model = Store
        url = serializers.HyperlinkedIdentityField(view_name="store", lookup_field="id")
        fields = ("id", "name", "description", "customer")


class Stores(ViewSet):
    """Request handlers for Stores"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """Handle GET requests to Store resource"""
        stores = Store.objects.all()

        serializer = StoreSerializer(stores, many=True, context={"request": request})
        return Response(serializer.data)
