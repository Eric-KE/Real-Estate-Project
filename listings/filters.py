from django_filters import rest_framework as filters
from django.db import models
from .models import Listing

class ListingFilter(filters.FilterSet):
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')

    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    min_bedrooms = filters.NumberFilter(field_name='bedrooms', lookup_expr='gte')
    min_bathrooms = filters.NumberFilter(field_name='bathrooms', lookup_expr='gte')

    search = filters.CharFilter(method='filter_by_keyword')

    class Meta:
        model = Listing
        fields = [ 'property_type', 'sale_type', 'location', 'bedrooms', 'bathrooms']

        def filter_by_keyword(self, queryset, name, value):
            return queryset.filter(
                models.Q(title__icontains=value) |
                models.Q(description__icontains=value)
            )