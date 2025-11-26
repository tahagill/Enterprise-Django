"""
Django signals for handling model events
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from .models import Order
from .email_utils import send_order_status_update_email
from .audit_utils import log_activity
import logging

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log user login activity."""
    log_activity(
        user=user,
        action='login',
        description=f'User {user.username} logged in',
        request=request
    )
    logger.info(f"User {user.username} logged in from {request.META.get('REMOTE_ADDR')}")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log user logout activity."""
    if user:
        log_activity(
            user=user,
            action='logout',
            description=f'User {user.username} logged out',
            request=request
        )
        logger.info(f"User {user.username} logged out")


@receiver(post_save, sender=User)
def log_user_signup(sender, instance, created, **kwargs):
    """Log new user signup."""
    if created:
        log_activity(
            user=instance,
            action='signup',
            description=f'New user {instance.username} registered'
        )
        logger.info(f"New user registered: {instance.username}")


@receiver(pre_save, sender=Order)
def track_order_status_change(sender, instance, **kwargs):
    """Track if order status has changed before saving."""
    if instance.pk:  # Only for existing orders
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            instance._status_changed = old_instance.status != instance.status
            instance._old_status = old_instance.status
        except Order.DoesNotExist:
            instance._status_changed = False
    else:
        instance._status_changed = False


@receiver(post_save, sender=Order)
def send_status_update_email(sender, instance, created, **kwargs):
    """Send email and log activity when order status is updated."""
    if created:
        # Log order creation
        log_activity(
            user=instance.user,
            action='order_created',
            description=f'Order created: {instance.title}',
            content_type='Order',
            object_id=instance.id
        )
        logger.info(f"Order {instance.id} created by {instance.user.username if instance.user else 'Anonymous'}")
    elif hasattr(instance, '_status_changed') and instance._status_changed:
        # Log order status change
        log_activity(
            user=instance.user,
            action='order_status_changed',
            description=f'Order {instance.title} status changed from {instance._old_status} to {instance.status}',
            content_type='Order',
            object_id=instance.id
        )
        logger.info(f"Order {instance.id} status changed from {instance._old_status} to {instance.status}")
        send_order_status_update_email(instance)

