from rest_framework import serializers
from .models import Listing, ListingImage
from users.serializers import UserSerializer

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'alt_text']

class ListingSerializer(serializers.ModelSerializer):
    agent_details = UserSerializer(source='agent', read_only=True)

    gallery = ListingImageSerializer(many=True, source='images', read_only=True)

    
    class Meta:
        model = Listing
        fields = [
            'id',
            'agent',
            'agent_details',
            'title',
            'description',
            'location',
            'price',
            'sale_type',
            'property_type',
            'bedrooms',
            'bathrooms',
            'sqft',
            'main_image',
            'gallery',
            'is_published',
            'created_at'
        ]
        read_only_fields = ['id', 'agent', 'created_at']

        