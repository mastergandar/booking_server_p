from django.shortcuts import get_object_or_404
from rest_framework import generics

from social.models import Review, Favorite, Report
from social.serializers import ReviewsSerializer, ReportSerializers, FavoriteSerializer, ReportMessagesSerializer


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewsSerializer


class ReviewsListView(generics.ListAPIView):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        return Review.objects.filter(content_type__model=self.kwargs.get('content_type'))


class ReviewUpdateRetrieveView(generics.RetrieveUpdateAPIView):
    serializer_class = ReviewsSerializer
    queryset = Review.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))


class ReportCreateView(generics.CreateAPIView):
    serializer_class = ReportSerializers


class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(content_type__model='properties')


class FavoriteRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))


class ReportsListView(generics.ListAPIView):
    serializer_class = ReportSerializers

    def get_queryset(self):
        return Report.objects.filter(content_type__model=self.kwargs.get('content_type'))


class ReportRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ReportSerializers
    queryset = Report.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))


class ReportMessagesListView(generics.ListAPIView):
    serializer_class = ReportMessagesSerializer

    def get_queryset(self):
        return Report.objects.filter(content_type__model='properties', object_id=self.kwargs.get('pk'),
                                     content_objec__user=self.request.user)
