from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="admin_dashboard"
    ),

    path(
        "products/",
        views.admin_products,
        name="admin_products"
    ),

    path(
        "products/add/",
        views.add_product,
        name="add_product"
    ),

    path(
        "products/<int:product_id>/edit/",
        views.edit_product,
        name="edit_product"
    ),

    path(
        "products/<int:product_id>/delete/",
        views.delete_product,
        name="delete_product"
    ),

    path(
        "orders/",
        views.admin_orders,
        name="admin_orders"
    ),

    path(
        "users/",
        views.admin_users,
        name="admin_users"
    ),
path(
    "orders/<int:order_id>/status/",
    views.update_order_status,
    name="update_order_status"
),
path(
    "users/<int:user_id>/activate/",
    views.activate_user,
    name="activate_user"
),

path(
    "users/<int:user_id>/deactivate/",
    views.deactivate_user,
    name="deactivate_user"
),

path(
    "users/<int:user_id>/delete/",
    views.delete_user,
    name="delete_user"
),

]