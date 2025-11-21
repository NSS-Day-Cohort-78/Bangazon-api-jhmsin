from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers
from bangazonapi.models import Store
from rest_framework.response import Response


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product category"""
    class Meta:
        model = Store
        url = serializers.HyperlinkedIdentityField(
            view_name='store',
            lookup_field='id'
        )
        fields = ( '__all__' )

class Stores(ViewSet):
    """Request handlers for Stores"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """Handle GET requests to Store resource"""  
        store = Store.objects.all()  

        serializer = StoreSerializer(
            store, many=True, context={'request': request}
        )
        return Response(serializer.data)