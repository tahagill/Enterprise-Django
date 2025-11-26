from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


class AuditLog(models.Model):
    """Model to track user activities and important actions."""
    
    ACTION_CHOICES = (
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('signup', 'User Signup'),
        ('profile_update', 'Profile Update'),
        ('password_change', 'Password Change'),
        ('order_created', 'Order Created'),
        ('order_updated', 'Order Updated'),
        ('order_status_changed', 'Order Status Changed'),
        ('contact_submitted', 'Contact Form Submitted'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, db_index=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Optional: Store related object information
    content_type = models.CharField(max_length=50, blank=True)  # e.g., 'Order', 'Contact'
    object_id = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp', 'action']),
            models.Index(fields=['user', '-timestamp']),
        ]
    
    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"{username} - {self.get_action_display()} at {self.timestamp}"


class SoftDeleteManager(models.Manager):
    """Custom manager to exclude soft-deleted items by default."""
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    """Abstract base model for soft delete functionality."""
    
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()  # Default manager excludes deleted
    all_objects = models.Manager()  # Manager that includes deleted items
    
    class Meta:
        abstract = True
    
    def delete(self, using=None, keep_parents=False, hard=False):
        """Soft delete by default, hard delete if hard=True."""
        if hard:
            super().delete(using=using, keep_parents=keep_parents)
        else:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save()
    
    def restore(self):
        """Restore a soft-deleted item."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class Contact(SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_index=True)
    name = models.CharField(max_length=122)
    email = models.EmailField(max_length=122, db_index=True)
    phone = PhoneNumberField(region=getattr(settings, 'PHONENUMBER_DEFAULT_REGION', None))  # Configurable region
    desc = models.TextField()
    date = models.DateField(db_index=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Order(SoftDeleteModel):
    PRIORITY_CHOICES = (
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
    )
    
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, db_index=True)

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, db_index=True)
    quantity = models.PositiveIntegerField()
    client_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='orders/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'status']),  # Composite index for common queries
            models.Index(fields=['user', '-created_at']),  # User's orders chronologically
        ]

    def __str__(self):
        return f"{self.title} - {self.client_name} ({self.status})"


class ServicePage(models.Model):
    """Model for configurable service page content."""
    
    # Singleton pattern - only one instance allowed
    title = models.CharField(max_length=200, default='Our Partners')
    heading = models.CharField(max_length=200, default="Let's Collaborate")
    content = models.TextField(
        help_text='Main service page content',
        default='At Enterprises, we take pride in being the trusted thread supplier...'
    )
    
    # Partner logos
    show_partner_logos = models.BooleanField(default=True, help_text='Show partner logos section')
    partner_section_title = models.CharField(max_length=200, default='Our Partners')
    
    # Meta information
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Service Page Content'
        verbose_name_plural = 'Service Page Content'
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        if not self.pk and ServicePage.objects.exists():
            raise ValidationError('There can only be one ServicePage instance')
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return 'Service Page Configuration'


class PartnerLogo(models.Model):
    """Model for partner logos displayed on services page."""
    
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/', help_text='Partner logo image')
    order = models.IntegerField(default=0, help_text='Display order (lower numbers appear first)')
    is_active = models.BooleanField(default=True, help_text='Show this logo on the page')
    url = models.URLField(blank=True, help_text='Optional link to partner website')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Partner Logo'
        verbose_name_plural = 'Partner Logos'
    
    def __str__(self):
        return self.name