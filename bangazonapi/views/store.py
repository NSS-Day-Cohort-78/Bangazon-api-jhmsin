from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers, status
from bangazonapi.models import Store
from rest_framework.response import Response
from .customer import Customer, CustomerUserSerializer
from .product import ProductSerializer

# class StoreProductsSerializer(serializers.ModelSerializer):
#     """JSON serializer"""
#     products = CustomerProductSerializer(many=True)

#     class Meta:
#         model = Customer
#         fields


class StoreOwnerSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    user = CustomerUserSerializer(many=False)
    products = ProductSerializer(many=True)

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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Request handler for store"""

        try:
            store = Store.objects.get(pk=pk)
            serializer = StoreSerializer(
                store, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Store.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
