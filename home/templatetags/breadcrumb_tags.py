"""
Template tags for breadcrumb navigation.
"""
from django import template
from django.urls import reverse, resolve

register = template.Library()


@register.inclusion_tag('breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    """
    Generate breadcrumb navigation based on current URL.
    Usage: {% breadcrumbs %}
    """
    request = context['request']
    path = request.path
    
    # Define breadcrumb mappings
    breadcrumb_map = {
        '/': [
            {'title': 'Home', 'url': None}
        ],
        '/about/': [
            {'title': 'Home', 'url': '/'},
            {'title': 'About Us', 'url': None}
        ],
        '/services/': [
            {'title': 'Home', 'url': '/'},
            {'title': 'Services', 'url': None}
        ],
        '/contact/': [
            {'title': 'Home', 'url': '/'},
            {'title': 'Contact Us', 'url': None}
        ],
        '/orders/': [
            {'title': 'Home', 'url': '/'},
            {'title': 'Place Order', 'url': None}
        ],
        '/status/': [
            {'title': 'Home', 'url': '/'},
            {'title': 'Order Status', 'url': None}
        ],
        '/search/': [
            {'title': 'Home', 'url': '/'},
            {'title': 'Order Status', 'url': '/status/'},
            {'title': 'Search', 'url': None}
        ],
        '/profile/': [
            {'title': 'Home', 'url': '/'},
            {'title': 'Profile', 'url': None}
        ],
        '/profile/edit/': [
            {'title': 'Home', 'url': '/'},
            {'title': 'Profile', 'url': '/profile/'},
            {'title': 'Edit Profile', 'url': None}
        ],
        '/profile/change-password/': [
            {'title': 'Home', 'url': '/'},
            {'title': 'Profile', 'url': '/profile/'},
            {'title': 'Change Password', 'url': None}
        ],
        '/login/': [
            {'title': 'Login', 'url': None}
        ],
        '/signup/': [
            {'title': 'Sign Up', 'url': None}
        ],
    }
    
    # Get breadcrumbs for current path
    breadcrumbs_list = breadcrumb_map.get(path, [
        {'title': 'Home', 'url': '/'}
    ])
    
    return {
        'breadcrumbs': breadcrumbs_list,
        'show_breadcrumbs': len(breadcrumbs_list) > 1
    }
