from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model

from products.models import Product
from orders.models import Order
from django.shortcuts import get_object_or_404
from .forms import ProductForm
User = get_user_model()
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from orders.models import Order
from notifications.services import notify_order_status


@staff_member_required
def update_order_status(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        new_status = request.POST.get("status")

        allowed_statuses = [
            "Pending",
            "Confirmed",
            "Packed",
            "Shipped",
            "Out for Delivery",
            "Delivered",
            "Cancelled",
        ]

        if new_status in allowed_statuses:

            # Remember the previous status
            old_status = order.status

            # Update order
            order.status = new_status
            order.save()

            # Send real-time notification to the customer
            notify_order_status(
                order,
                old_status,
            )

            messages.success(
                request,
                f"Order #{order.id} status updated to {new_status}."
            )

        else:

            messages.error(
                request,
                "Invalid order status."
            )

    return redirect("adminpanel:orders")



@staff_member_required
def dashboard(request):

    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    total_users = User.objects.count()

    revenue = sum(
        order.total_amount
        for order in Order.objects.all()
    )

    recent_orders = Order.objects.order_by(
        "-created_at"
    )[:5]

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_users": total_users,
        "revenue": revenue,
        "recent_orders": recent_orders,
    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context
    )


@staff_member_required
def admin_products(request):

    products = Product.objects.all()

    return render(
        request,
        "adminpanel/products.html",
        {
            "products": products
        }
    )


@staff_member_required
def admin_orders(request):

    orders = Order.objects.order_by(
        "-created_at"
    )

    return render(
        request,
        "adminpanel/orders.html",
        {
            "orders": orders
        }
    )


@staff_member_required
def admin_users(request):

    users = User.objects.all()

    return render(
        request,
        "adminpanel/users.html",
        {
            "users": users
        }
    )
@staff_member_required
def add_product(request):

    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product added successfully!"
            )

            return redirect("admin_products")

    else:

        form = ProductForm()

    return render(
        request,
        "adminpanel/product_form.html",
        {
            "form": form,
            "title": "Add Product"
        }
    )


@staff_member_required
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product updated successfully!"
            )

            return redirect("admin_products")

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "adminpanel/product_form.html",
        {
            "form": form,
            "title": "Edit Product"
        }
    )


@staff_member_required
def delete_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Product deleted successfully!"
        )

        return redirect("admin_products")

    return render(
        request,
        "adminpanel/delete_product.html",
        {
            "product": product
        }
    )

@staff_member_required
def update_order_status(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        new_status = request.POST.get("status")

        allowed_statuses = [
            "Pending",
            "Confirmed",
            "Processing",
            "Shipped",
            "Delivered",
            "Cancelled",
        ]

        if new_status in allowed_statuses:

            from notifications.services import notify_order_status

            old_status = order.status

            order.status = new_status
            order.save()

            notify_order_status(
                order,
                old_status,
            )
            messages.success(
                request,
                f"Order #{order.id} status updated to {new_status}."
            )

        else:

            messages.error(
                request,
                "Invalid order status."
            )

    return redirect("admin_orders")

@staff_member_required
def admin_users(request):

    users = User.objects.all().order_by("-date_joined")

    return render(
        request,
        "adminpanel/users.html",
        {
            "users": users
        }
    )
# =====================================
# ACTIVATE USER
# =====================================

@staff_member_required
def activate_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    user.is_active = True
    user.save()

    messages.success(
        request,
        f"{user.username} has been activated."
    )

    return redirect("admin_users")


# =====================================
# DEACTIVATE USER
# =====================================

@staff_member_required
def deactivate_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    # Prevent admin from disabling themselves
    if user == request.user:

        messages.error(
            request,
            "You cannot deactivate your own account."
        )

        return redirect("admin_users")

    user.is_active = False
    user.save()

    messages.success(
        request,
        f"{user.username} has been deactivated."
    )

    return redirect("admin_users")


# =====================================
# DELETE USER
# =====================================

@staff_member_required
def delete_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    if user == request.user:

        messages.error(
            request,
            "You cannot delete your own account."
        )

        return redirect("admin_users")

    if request.method == "POST":

        username = user.username

        user.delete()

        messages.success(
            request,
            f"{username} has been deleted."
        )

        return redirect("admin_users")

    return render(
        request,
        "adminpanel/delete_user.html",
        {
            "user": user
        }
    )