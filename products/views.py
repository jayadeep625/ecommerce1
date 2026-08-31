from django.shortcuts import render, get_object_or_404
from .models import Product


def product_list(request):

    products = Product.objects.all()

    # Search
    search = request.GET.get("search")

    if search:
        products = products.filter(name__icontains=search)

    # Sort
    sort = request.GET.get("sort")

    if sort == "low":
        products = products.order_by("price")

    elif sort == "high":
        products = products.order_by("-price")

    elif sort == "name":
        products = products.order_by("name")

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "search": search,
            "sort": sort,
        },
    )


def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product
        },
    )