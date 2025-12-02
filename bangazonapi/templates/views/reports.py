from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import Round
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from bangazonapi.models import Order, Product, Customer, Favorite


class Reports(ViewSet):
    @action(detail=False, methods=["get"], url_path="expensiveproducts")
    def expensive_products_report(self, request):
        expensive_products = Product.objects.filter(price__gte=1000)
        context = {"products": expensive_products}
        return render(request, "reports/expensive_products.html", context)

    @action(detail=False, methods=["get"], url_path="inexpensiveproducts")
    def inexpensive_products_report(self, request):
        inexpensive_products = Product.objects.filter(price__lt=1000)
        context = {"products": inexpensive_products}
        return render(request, "reports/inexpensive_products.html", context)

    @action(detail=False, methods=["get"], url_path="orders")
    def orders(self, request):

        order_status = request.query_params.get("status")

        if order_status is not None and order_status == "incomplete":

            incomplete_orders = Order.objects.filter(payment_type=None).annotate(
                total_price=Round(Sum("lineitems__product__price"), 2)
            )

            context = {"orders": incomplete_orders}
            return render(request, "reports/incomplete_orders.html", context)

        elif order_status is not None and order_status == "complete":

            complete_orders = Order.objects.exclude(completed_on=None).annotate(
                total_price=Round(Sum("lineitems__product__price"), 2)
            )
            context = {"orders": complete_orders}
            return render(request, "reports/completed_orders.html", context)

    @action(detail=False, methods=["get"], url_path="favoritesellers")
    def favorite_sellers(self, request):
  
        favorites = Favorite.objects.prefetch_related("customer").all()
        customers = []
        for favorite in favorites:
            customers.append(favorite.customer)

        customers = list(set(customers))
        context = {"favorites": favorites, "customers": customers}
        return render(request, "reports/favorite_sellers.html", context)