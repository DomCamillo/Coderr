from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    location = models.CharField(max_length=100, default='', null=True, blank=True)
    tel = models.CharField(max_length=20, null=True,default='', blank=True)
    description = models.TextField( blank=True, default='')
    working_hours = models.CharField(max_length=100, default='', blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username