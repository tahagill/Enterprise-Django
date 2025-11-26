"""
Utility functions for audit logging.
"""
from home.models import AuditLog


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """Extract user agent from request."""
    return request.META.get('HTTP_USER_AGENT', '')[:255]


def log_activity(user, action, description='', request=None, content_type='', object_id=None):
    """
    Create an audit log entry.
    
    Args:
        user: User object or None for anonymous
        action: Action type (must be in AuditLog.ACTION_CHOICES)
        description: Optional description of the action
        request: Optional request object to extract IP and user agent
        content_type: Optional related object type (e.g., 'Order', 'Contact')
        object_id: Optional related object ID
    
    Returns:
        AuditLog instance
    """
    ip_address = None
    user_agent = ''
    
    if request:
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
    
    audit_log = AuditLog.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
        content_type=content_type,
        object_id=object_id
    )
    
    return audit_log
