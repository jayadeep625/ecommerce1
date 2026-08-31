from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Wishlist
from products.models import Product


@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect("wishlist")


@login_required
def remove_from_wishlist(request, wishlist_id):

    item = get_object_or_404(
        Wishlist,
        id=wishlist_id,
        user=request.user
    )

    item.delete()

    return redirect("wishlist")


@login_required
def wishlist(request):

    items = Wishlist.objects.filter(user=request.user)

    return render(
        request,
        "wishlist/wishlist.html",
        {
            "items": items
        }
    )