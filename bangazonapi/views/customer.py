from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Customer, Product
from django.contrib.auth.models import User

class CustomerUserSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', )

class CustomerProductSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Product
        fields = ( 'quantity', )

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers"""
    user = CustomerUserSerializer(many=False)
    products = CustomerProductSerializer(many=True)

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer', lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'phone_number', 'address', 'products', 'store')
        depth = 1


class Customers(ViewSet):

    def update(self, request, pk=None):
        """
        @api {PUT} /customers/:id PUT changes to customer profile
        @apiName UpdateCustomer
        @apiGroup Customer

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {id} id Customer Id to update
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        customer = Customer.objects.get(user=request.auth.user)
        customer.user.last_name = request.data["last_name"]
        customer.user.email = request.data["email"]
        customer.address = request.data["address"]
        customer.phone_number = request.data["phone_number"]
        customer.user.save()
        customer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
