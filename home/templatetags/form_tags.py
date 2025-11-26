"""
Custom template tags and filters for Bootstrap form rendering.
"""
from django import template
from django.forms import BoundField
from django.forms.widgets import CheckboxInput, RadioSelect, CheckboxSelectMultiple, FileInput

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Add CSS class to a form field.
    Usage: {{ form.field|add_class:"form-control" }}
    """
    if isinstance(field, BoundField):
        return field.as_widget(attrs={'class': css_class})
    return field


@register.filter(name='add_placeholder')
def add_placeholder(field, placeholder):
    """
    Add placeholder text to a form field.
    Usage: {{ form.field|add_placeholder:"Enter your name" }}
    """
    if isinstance(field, BoundField):
        return field.as_widget(attrs={'placeholder': placeholder})
    return field


@register.filter(name='bootstrap_field')
def bootstrap_field(field):
    """
    Automatically apply Bootstrap classes to form fields.
    Usage: {{ form.field|bootstrap_field }}
    """
    if not isinstance(field, BoundField):
        return field
    
    widget = field.field.widget
    css_class = field.css_classes()
    
    # Different styling for different widget types
    if isinstance(widget, CheckboxInput):
        return field.as_widget(attrs={'class': 'form-check-input'})
    elif isinstance(widget, (RadioSelect, CheckboxSelectMultiple)):
        return field.as_widget(attrs={'class': 'form-check-input'})
    elif isinstance(widget, FileInput):
        return field.as_widget(attrs={'class': 'form-control'})
    else:
        # Default form-control for text inputs, selects, textareas
        classes = 'form-control'
        if field.errors:
            classes += ' is-invalid'
        return field.as_widget(attrs={'class': classes})


@register.inclusion_tag('form_snippets/field.html')
def render_field(field, show_label=True, placeholder=''):
    """
    Render a complete Bootstrap form field with label, input, and errors.
    Usage: {% render_field form.field %}
    """
    return {
        'field': field,
        'show_label': show_label,
        'placeholder': placeholder,
    }


@register.inclusion_tag('form_snippets/errors.html')
def render_errors(field):
    """
    Render field errors in Bootstrap alert format.
    Usage: {% render_errors form.field %}
    """
    return {'field': field}


@register.filter(name='is_checkbox')
def is_checkbox(field):
    """Check if field is a checkbox."""
    return isinstance(field.field.widget, CheckboxInput)


@register.filter(name='is_radio')
def is_radio(field):
    """Check if field is a radio button."""
    return isinstance(field.field.widget, RadioSelect)


@register.filter(name='is_file')
def is_file(field):
    """Check if field is a file input."""
    return isinstance(field.field.widget, FileInput)
