from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc =  models.TextField()
    date = models.DateField()
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=20)


    def __str__(self):
        return self.name

class Order(models.Model):
    PRIORITY_CHOICES = (
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    quantity = models.PositiveIntegerField()
    client_name = models.CharField(max_length=255)
    ##file = models.FileField(upload_to='uploads/', blank=True, null=True)    will use it later 

    def __str__(self):
        return self.title
