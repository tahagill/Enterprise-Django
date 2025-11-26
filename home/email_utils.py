"""
Email utility functions for sending notifications
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
import logging

logger = logging.getLogger(__name__)


def send_welcome_email(user, request=None):
    """Send welcome email to newly registered user."""
    try:
        site_url = 'http://localhost:8000'  # Default
        if request:
            site_url = f"http://{get_current_site(request).domain}"
        
        context = {
            'user': user,
            'site_url': site_url,
        }
        
        html_message = render_to_string('emails/welcome_email.html', context)
        
        send_mail(
            subject='Welcome to Enterprise!',
            message=f'Hello {user.username}, welcome to Enterprise!',  # Plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@enterprise.com',
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Welcome email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")
        return False


def send_order_confirmation_email(order, request=None):
    """Send order confirmation email to user."""
    try:
        if not order.user or not order.user.email:
            logger.warning(f"Cannot send order confirmation - no user email for order {order.id}")
            return False
        
        site_url = 'http://localhost:8000'  # Default
        if request:
            site_url = f"http://{get_current_site(request).domain}"
        
        context = {
            'order': order,
            'order_status_url': f"{site_url}/status/",
        }
        
        html_message = render_to_string('emails/order_confirmation.html', context)
        
        send_mail(
            subject=f'Order Confirmation - {order.title}',
            message=f'Your order "{order.title}" has been received and is being processed.',
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@enterprise.com',
            recipient_list=[order.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Order confirmation email sent for order {order.id} to {order.user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send order confirmation for order {order.id}: {str(e)}")
        return False


def send_order_status_update_email(order, request=None):
    """Send order status update email to user."""
    try:
        if not order.user or not order.user.email:
            logger.warning(f"Cannot send status update - no user email for order {order.id}")
            return False
        
        site_url = 'http://localhost:8000'  # Default
        if request:
            site_url = f"http://{get_current_site(request).domain}"
        
        context = {
            'order': order,
            'order_status_url': f"{site_url}/status/",
        }
        
        html_message = render_to_string('emails/order_status_update.html', context)
        
        send_mail(
            subject=f'Order Status Update - {order.title}',
            message=f'Your order "{order.title}" status has been updated to: {order.status}',
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@enterprise.com',
            recipient_list=[order.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Status update email sent for order {order.id} to {order.user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send status update for order {order.id}: {str(e)}")
        return False


def send_contact_confirmation_email(contact):
    """Send confirmation email after contact form submission."""
    try:
        if not contact.email:
            logger.warning(f"Cannot send contact confirmation - no email for contact {contact.id}")
            return False
        
        context = {
            'contact': contact,
        }
        
        html_message = render_to_string('emails/contact_confirmation.html', context)
        
        send_mail(
            subject='Thank you for contacting Enterprise',
            message=f'Hello {contact.name}, we have received your message and will get back to you soon.',
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@enterprise.com',
            recipient_list=[contact.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Contact confirmation email sent to {contact.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send contact confirmation to {contact.email}: {str(e)}")
        return False
