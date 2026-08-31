from notifications.services import notify_admins
import uuid
from decimal import Decimal

import razorpay

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from cart.models import Cart
from .models import Order, OrderItem, Address
from .forms import AddressForm


User = get_user_model()


# ==========================================================
# RAZORPAY CLIENT
# ==========================================================

razorpay_client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET,
    )
)


# ==========================================================
# CHECKOUT
# ==========================================================

@login_required
def checkout(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    addresses = Address.objects.filter(
        user=request.user
    )

    selected_address = request.session.get(
        "selected_address"
    )

    subtotal = sum(
        (
            item.product.price * item.quantity
            for item in cart_items
        ),
        Decimal("0")
    )

    shipping = Decimal("0")
    discount = Decimal("0")

    total = subtotal + shipping - discount

    context = {
        "cart_items": cart_items,
        "addresses": addresses,
        "selected_address": selected_address,
        "subtotal": subtotal,
        "shipping": shipping,
        "discount": discount,
        "total": total,
    }

    return render(
        request,
        "orders/checkout.html",
        context
    )


# ==========================================================
# ADD ADDRESS
# ==========================================================

@login_required
def add_address(request):

    if request.method == "POST":

        form = AddressForm(request.POST)

        if form.is_valid():

            address = form.save(commit=False)

            address.user = request.user

            address.save()

            return redirect("checkout")

    else:

        form = AddressForm()

    return render(
        request,
        "orders/address_form.html",
        {
            "form": form
        }
    )


# ==========================================================
# SELECT ADDRESS
# ==========================================================

@login_required
def select_address(request, address_id):

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    request.session["selected_address"] = address.id

    return redirect("checkout")


# ==========================================================
# PAYMENT PAGE
# ==========================================================

@login_required
def payment(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():
        return redirect("cart")

    address_id = request.session.get(
        "selected_address"
    )

    if not address_id:

        messages.error(
            request,
            "Please select an address first."
        )

        return redirect("checkout")

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    total = sum(
        (
            item.product.price * item.quantity
            for item in cart_items
        ),
        Decimal("0")
    )

    if request.method == "POST":

        payment_method = request.POST.get(
            "payment"
        )

        if payment_method == "COD":

            request.session["payment"] = "COD"

            return redirect("place_order")

        if payment_method == "Razorpay":

            # ------------------------------------------
            # Convert INR to paise
            # ------------------------------------------

            amount_paise = int(
                total * 100
            )

            # ------------------------------------------
            # Create Razorpay Order
            # ------------------------------------------

            receipt = (
                f"rcpt_{request.user.id}_"
                f"{uuid.uuid4().hex[:12]}"
            )

            razorpay_order = razorpay_client.order.create(
                {
                    "amount": amount_paise,
                    "currency": "INR",
                    "receipt": receipt,
                }
            )

            # ------------------------------------------
            # Create local Django order
            # ------------------------------------------

            order = Order.objects.create(

                user=request.user,

                address_obj=address,

                full_name=address.full_name,

                phone=address.phone,

                address=(
                    f"{address.house}, "
                    f"{address.street}"
                ),

                city=address.city,

                state=address.state,

                pincode=address.pincode,

                payment_method="Razorpay",

                total_amount=total,

                status="Pending",

                razorpay_order_id=razorpay_order["id"],
            )

            # ------------------------------------------
            # Save pending order in session
            # ------------------------------------------

            request.session[
                "pending_razorpay_order_id"
            ] = order.id

            return render(
                request,
                "orders/payment.html",
                {
                    "order": order,
                    "razorpay_order_id":
                        razorpay_order["id"],
                    "razorpay_key":
                        settings.RAZORPAY_KEY_ID,
                    "amount":
                        amount_paise,
                    "amount_display":
                        total,
                    "user_name":
                        request.user.get_full_name()
                        or request.user.username,
                    "user_email":
                        request.user.email,
                    "user_phone":
                        address.phone,
                }
            )

        messages.error(
            request,
            "Please select a valid payment method."
        )

    return render(
        request,
        "orders/payment.html",
        {
            "address": address,
            "total": total,
        }
    )


# ==========================================================
# COD PLACE ORDER
# ==========================================================

@login_required
def place_order(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():

        return redirect("cart")

    address_id = request.session.get(
        "selected_address"
    )

    if not address_id:

        return redirect("checkout")

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    payment_method = request.session.get(
        "payment",
        "COD"
    )

    total = sum(
        (
            item.product.price * item.quantity
            for item in cart_items
        ),
        Decimal("0")
    )

    order = Order.objects.create(

        user=request.user,

        address_obj=address,

        full_name=address.full_name,

        phone=address.phone,

        address=(
            f"{address.house}, "
            f"{address.street}"
        ),

        city=address.city,

        state=address.state,

        pincode=address.pincode,

        payment_method=payment_method,

        total_amount=total,

        status="Pending",
    )

    for item in cart_items:

        OrderItem.objects.create(

            order=order,

            product=item.product,

            quantity=item.quantity,

            price=item.product.price,
        )

    cart_items.delete()
    # ==========================================
    # NOTIFY ADMINS
    # ==========================================

    notify_admins(
        title="New Order Received",
        message=(
            f"{request.user.get_full_name() or request.user.username} "
            f"placed Order #{order.id} "
            f"for ₹{order.total_amount}."
        ),
        notification_type="new_order",
    )

    request.session.pop(
        "selected_address",
        None
    )

    request.session.pop(
        "payment",
        None
    )

    return redirect(
        "order_success"
    )


# ==========================================================
# RAZORPAY SUCCESS CALLBACK
# ==========================================================

@csrf_exempt
@login_required
def razorpay_callback(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "error": "Invalid request method"
            },
            status=405
        )

    payment_id = request.POST.get(
        "razorpay_payment_id"
    )

    razorpay_order_id = request.POST.get(
        "razorpay_order_id"
    )

    signature = request.POST.get(
        "razorpay_signature"
    )

    if not payment_id or not razorpay_order_id or not signature:

        messages.error(
            request,
            "Payment information is incomplete."
        )

        return redirect("checkout")

    # ------------------------------------------
    # Get local order
    # ------------------------------------------

    local_order_id = request.session.get(
        "pending_razorpay_order_id"
    )

    if not local_order_id:

        messages.error(
            request,
            "Payment order could not be found."
        )

        return redirect("checkout")

    order = get_object_or_404(
        Order,
        id=local_order_id,
        user=request.user
    )

    # ------------------------------------------
    # Compare Razorpay order ID with our DB
    # ------------------------------------------

    if order.razorpay_order_id != razorpay_order_id:

        messages.error(
            request,
            "Payment order verification failed."
        )

        return redirect("checkout")

    # ------------------------------------------
    # Verify Razorpay signature
    # ------------------------------------------

    try:

        razorpay_client.utility.verify_payment_signature(
            {
                "razorpay_order_id":
                    order.razorpay_order_id,

                "razorpay_payment_id":
                    payment_id,

                "razorpay_signature":
                    signature,
            }
        )

    except razorpay.errors.SignatureVerificationError:

        order.status = "Cancelled"

        order.save(
            update_fields=["status"]
        )

        messages.error(
            request,
            "Payment verification failed."
        )

        return redirect("checkout")

    # ------------------------------------------
    # Store payment information
    # ------------------------------------------

    order.razorpay_payment_id = payment_id

    order.razorpay_signature = signature

    order.status = "Confirmed"

    order.save()

    # ------------------------------------------
    # Create OrderItems
    # ------------------------------------------

    cart_items = Cart.objects.filter(
        user=request.user
    )

    for item in cart_items:

        OrderItem.objects.create(

            order=order,

            product=item.product,

            quantity=item.quantity,

            price=item.product.price,
        )
    notify_admins(
        title="New Order Received",
        message=(
            f"{request.user.get_full_name() or request.user.username} "
            f"placed Order #{order.id} "
            f"for ₹{order.total_amount}."
        ),
        notification_type="new_order",
    )
    # ------------------------------------------
    # Empty cart
    # ------------------------------------------

    cart_items.delete()

    # ------------------------------------------
    # Clear sessions
    # ------------------------------------------

    request.session.pop(
        "selected_address",
        None
    )

    request.session.pop(
        "payment",
        None
    )

    request.session.pop(
        "pending_razorpay_order_id",
        None
    )

    return redirect(
        "order_success"
    )


# ==========================================================
# ORDER SUCCESS
# ==========================================================

@login_required
def order_success(request):

    return render(
        request,
        "orders/order_success.html"
    )


# ==========================================================
# MY ORDERS
# ==========================================================

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders
        }
    )


# ==========================================================
# ORDER DETAILS
# ==========================================================

@login_required
def order_details(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "orders/order_details.html",
        {
            "order": order
        }
    )


# ==========================================================
# CANCEL ORDER
# ==========================================================

@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status in [
        "Pending",
        "Confirmed"
    ]:

        order.status = "Cancelled"

        order.save()

        messages.success(
            request,
            "Your order has been cancelled successfully."
        )

    else:

        messages.error(
            request,
            "This order can no longer be cancelled."
        )

    return redirect(
        "order_details",
        order_id=order.id
    )