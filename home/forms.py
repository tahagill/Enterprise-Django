from django import forms
from .models import Order
from django.core.exceptions import ValidationError

def validate_file_size(value):
    """Validate file size (max 5MB)."""
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError('File size cannot exceed 5MB.')

def validate_file_type(value):
    """Validate file type (images and documents only)."""
    allowed_types = [
        'image/jpeg', 'image/png', 'image/gif', 'image/webp',
        'application/pdf', 'application/msword', 
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
    if hasattr(value, 'content_type') and value.content_type not in allowed_types:
        raise ValidationError('Unsupported file type. Only images and documents are allowed.')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'client_name', 'priority', 'quantity', 'description', 'file']
        labels = {
            'title': 'Order Title',
            'client_name': 'Client Name',
            'priority': 'Priority Level',
            'quantity': 'Quantity',
            'description': 'Order Description',
            'file': 'Attachment (Optional)',
        }
        help_texts = {
            'file': 'Upload images or documents (max 5MB). Supported formats: JPG, PNG, GIF, PDF, DOC, DOCX',
            'description': 'Provide detailed information about your order requirements',
            'quantity': 'Enter the number of items needed',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g., Custom T-Shirt Order'
        })
        self.fields['client_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g., John Doe'
        })
        self.fields['priority'].widget.attrs.update({'class': 'form-select'})
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g., 100',
            'min': '1'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe your order in detail...'
        })
        self.fields['file'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].validators.append(validate_file_size)
        self.fields['file'].validators.append(validate_file_type)