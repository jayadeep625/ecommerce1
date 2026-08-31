from django.urls import path
from . import views

urlpatterns = [
    # Checkout Page
    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),

    # Add New Address
    path(
        "address/add/",
        views.add_address,
        name="add_address",
    ),

    # Select Address
    path(
        "select-address/<int:address_id>/",
        views.select_address,
        name="select_address",
    ),

    # Payment Page
    path(
        "payment/",
        views.payment,
        name="payment",
    ),

    # Place Order
    path(
        "place-order/",
        views.place_order,
        name="place_order",
    ),

    # Order Success
    path(
        "success/",
        views.order_success,
        name="order_success",
    ),
path(
    "my-orders/",
    views.my_orders,
    name="my_orders",
),
path(
    "details/<int:order_id>/",
    views.order_details,
    name="order_details",
),
path(
    "cancel/<int:order_id>/",
    views.cancel_order,
    name="cancel_order",
),
path(
    "razorpay-callback/",
    views.razorpay_callback,
    name="razorpay_callback"
),
]