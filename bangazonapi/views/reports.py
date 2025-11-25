from django.shortcuts import render
from bangazonapi.models import Product

def expensive_products_report(request):
    expensive_products = Product.objects.filter(price__gte=1000)
    context = {'products': expensive_products}
    return render(request, 'reports/expensive_products.html', context)

