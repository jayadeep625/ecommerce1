from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Notification


@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")[:50]

    data = []

    for notification in notifications:

        data.append({
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "notification_type": notification.notification_type,
            "is_read": notification.is_read,
            "created_at": notification.created_at.isoformat(),
        })

    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).count()

    return JsonResponse({
        "notifications": data,
        "unread_count": unread_count,
    })


@login_required
@require_POST
def mark_notification_read(
    request,
    notification_id,
):

    notification = Notification.objects.filter(
        id=notification_id,
        user=request.user,
    ).first()

    if not notification:
        return JsonResponse(
            {
                "success": False,
                "error": "Notification not found.",
            },
            status=404,
        )

    notification.is_read = True
    notification.save(
        update_fields=["is_read"]
    )

    return JsonResponse({
        "success": True,
    })


@login_required
@require_POST
def mark_all_notifications_read(request):

    Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).update(
        is_read=True
    )

    return JsonResponse({
        "success": True,
    })