from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Listing, ListingImage
from .serializer import ListingSerializer, ListingImageSerializer
from .filters import ListingFilter


# Create your views here.

class IsAgentOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.role == 'agent'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.agent == request.user
    

class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = ListingSerializer
    permission_classes = [IsAgentOrReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter ]
    filterset_class = ListingFilter


    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)



class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAgentOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)

class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAgentOrReadOnly]


class ListingImageUploadView(generics.CreateAPIView):
    queryset = ListingImage.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [ permissions.IsAuthenticated, IsAgentOrReadOnly]

    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *files, **kwargs):
        try:
            listing = Listing.objects.get(pk=self.kwargs.get('pk'))
        except Listing.DoesNotExist:
            return Response({
                'error': 'Listing Not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, listing)

        uploaded_files = request.FILES.getlist('image')
        if not uploaded_files:
            return Response({
                'error': 'No image were provided'
            }, status=status.HTTP_400_BAD_REQUEST)

        created_images = []
        for file_data in uploaded_files:
            img = ListingImage.objects.create(
                listing=listing,
                image=file_data,
                alt_text=request.data.get('alt_text', f"Image for {listing.title}")
            )
            created_images.append(ListingImageSerializer(img).data)

        return Response(created_images, status=status.HTTP_201_CREATED)

        