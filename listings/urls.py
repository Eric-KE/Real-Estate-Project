from django.urls import path
from .views import ListingListCreateView, ListingDetailView, ListingImageUploadView

urlpatterns = [
    path('', ListingListCreateView.as_view(), name='listing-list-create'),
    path('<int:pk>', ListingDetailView.as_view(), name='listing-details'),
    path('<int:pk>/upload-images/', ListingImageUploadView.as_view(), name="listing-image-upload")
]

