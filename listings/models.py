from django.db import models
from django.conf import settings

# Create your models here.

class Listing(models.Model):
    SALE_TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('townhouse', 'Townhouse'),
        ('land', 'Land'),
    ]

    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_type = models.CharField(max_length=10, choices=SALE_TYPE_CHOICES, default='sale')
    property_type = models.CharField(max_length=15, choices=PROPERTY_TYPE_CHOICES, default='house')


    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    sqft = models.IntegerField(default=0)
    main_image = models.ImageField(upload_to='properties', null=True, blank=True)

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upsdated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} - {self.location} ({self.price})"


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/gallery/')
    alt_text = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Image for { self.listing.title }"