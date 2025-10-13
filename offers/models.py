from django.db import models
from django.contrib.auth.models import User



class OfferDetails(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()

class Offer(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='offers/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digigts=100, decimal_places=2)
    min_delivery_time = models.DurationField()
    details = models.ForeignKey(OfferDetails, on_delete=models.CASCADE, related_name='offers')

    def __str__(self):
        return self.title

