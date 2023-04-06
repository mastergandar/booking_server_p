from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from core.permissions import IsOwner
from file_manager.models import LinkedImages
from file_manager.serializers import LinkedImagesSerializer


class LinkedImagesListCreateView(generics.ListCreateAPIView):
    serializer_class = LinkedImagesSerializer
    filterset_fields = ['content_type', 'object_id']

    def get_queryset(self):
        queryset = LinkedImages.objects.filter(user=self.request.user)
        return queryset


class LinkedImagesRetrieveView(generics.RetrieveUpdateAPIView):
    serializer_class = LinkedImagesSerializer
    queryset = LinkedImages.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        if self.request.method == 'PUT':
            self.permission_classes = [IsOwner()]
        return super().get_permissions()

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))
