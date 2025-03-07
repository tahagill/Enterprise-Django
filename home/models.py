from django.db import models
from django.contrib.auth.models import User  # Added

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Added
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()
    # Removed password and username fields

class Order(models.Model):
    PRIORITY_CHOICES = (
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    quantity = models.PositiveIntegerField()
    client_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='orders/', blank=True, null=True)