from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

from .models import Notification


User = get_user_model()


def create_notification(
    user,
    title,
    message,
    notification_type="general",
):
    """
    Save notification in database
    and send it immediately through WebSocket.
    """

    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
    )

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "notification_id": notification.id,
            "title": title,
            "message": message,
            "notification_type": notification_type,
            "created_at": notification.created_at.isoformat(),
        },
    )

    return notification


def get_admin_users():
    """
    Return active staff/admin users.
    """

    return User.objects.filter(
        is_staff=True,
        is_active=True,
    )


def notify_admins(
    title,
    message,
    notification_type="order",
):
    """
    Send one notification to every active admin.
    """

    for admin in get_admin_users():
        create_notification(
            user=admin,
            title=title,
            message=message,
            notification_type=notification_type,
        )


def notify_order_status(order, old_status):
    """
    Notify the customer whenever the admin changes
    the order status.
    """

    if old_status == order.status:
        return

    status_messages = {
        "Confirmed": (
            "Order Confirmed",
            f"Your Order #{order.id} has been confirmed.",
        ),

        "Packed": (
            "Order Packed",
            f"Your Order #{order.id} has been packed.",
        ),

        "Shipped": (
            "Order Shipped",
            f"Your Order #{order.id} has been shipped.",
        ),

        "Out for Delivery": (
            "Out for Delivery",
            f"Your Order #{order.id} is out for delivery.",
        ),

        "Delivered": (
            "Order Delivered",
            f"Your Order #{order.id} has been delivered.",
        ),

        "Cancelled": (
            "Order Cancelled",
            f"Your Order #{order.id} has been cancelled.",
        ),
    }

    if order.status not in status_messages:
        return

    title, message = status_messages[order.status]

    create_notification(
        user=order.user,
        title=title,
        message=message,
        notification_type="order_status",
    )