from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    file = models.ImageField(upload_to='profiles/', null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    tel_number = models.CharField(max_length=20, null=True, blank=True)
    working_hours = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username