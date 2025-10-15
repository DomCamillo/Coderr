from django.db import models


class Order (models.Model):
        STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
    ]

        OFFER_TYPE_CHOICES = [
         ('basic', 'Basic'),
         ('standard', 'Standard'),
         ('premium', 'Premium'),
            ]

        """Kopierte Felder von Offerdetails"""
        offer_detail = models.ForeignKey('offers.OfferDetails', on_delete=models.CASCADE)
        title = models.CharField(max_length=200)
        revisions = models.IntegerField(default=0)
        delivery_time_in_days = models.IntegerField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
        features = models.JSONField()
        offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default='basic')

        """"Order spezifische Felder"""
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"Order {self.id} - {self.title} - {self.status}"