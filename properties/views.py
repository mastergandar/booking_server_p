import random
from itertools import chain

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework.filters import CharFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from post_office import mail
from rest_framework import generics, status, filters
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from core.pagination import StandardResultsSetPagination
from core.permissions import IsOwner
from payments.enums import TransactionStatus
from payments.models import Orders, PromotionObjects
from payments.serializers import OrderSerializer
from properties.enums import Status
from properties.filters import PropertiesFilterSet, NullsAlwaysLastOrderingFilter, PropertyOrderFilterSet, \
    PropertyOccupationsFilterSet
from properties.models import Properties, Rules, Amenities
from properties.serializers import PropertiesSerializer, SmallPropertiesSerializer, RulesSerializer, \
    AmenitiesSerializer, PropertiesPromotionSerializer
from properties.service import PropertyService


class PropertiesFilter(FilterSet):

    amenities = CharFilter(method="by_amenities")

    class Meta:
        models = Properties

    def by_amenities(self, queryset, name, amenities: str):

        if amenities:
            amenities_list = []
            for amenity in amenities.split(','):
                amenities_list.append(amenity)

            queryset = queryset.filter(amenities__in=amenities_list)
        return queryset.order_by('-id')


class PropertiesListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SmallPropertiesSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [NullsAlwaysLastOrderingFilter, filters.SearchFilter]
    filterset_class = PropertiesFilterSet
    search_filter = [
        'user',
        'title',
        'accommodation_type',
        'flat_type',
        'house_type',
        'room_type',
        'unique_type',
        'hotel_type',
        'rent_type',
        'guests_count',
        'bedrooms_count',
        'beds_count',
        'bathrooms_count',
        'is_available',
        'arrival_time',
        'departure_time',
        'price'
    ]
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = Properties.objects.all()
        queryset = PropertyService().query_filter(
            queryset,
            self.request.query_params.get('accommodation_type', ''),
            self.request.query_params.get('flat_type', ''),
            self.request.query_params.get('house_type', ''),
            self.request.query_params.get('room_type', ''),
            self.request.query_params.get('unique_type', ''),
            self.request.query_params.get('hotel_type', ''),
            self.request.query_params.get('rent_type', ''),
            self.request.query_params.get('guests_count', ''),
            self.request.query_params.get('bedrooms_count', ''),
            self.request.query_params.get('beds_count', ''),
            self.request.query_params.get('bathrooms_count', ''),
        )
        return queryset.order_by('-id')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        promotion_list = []
        try:
            promotions_sample = random.sample(
                PromotionObjects.objects.all(), min(len(PromotionObjects.objects.all()), 10)
            )
            promotion_list.append(PromotionObjects.objects.filter(id__in=promotions_sample))
        except (ValueError, TypeError) as e:
            print(f"Promotion views error: {e}")
        response.data['promotion_list'] = promotion_list

        return response


class PropertiesListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SmallPropertiesSerializer
        if self.request.method == 'POST':
            return PropertiesSerializer

    def get_queryset(self):
        queryset = Properties.objects.filter(user=self.request.user)
        return queryset


class PropertyUpdateRetrieveDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertiesSerializer
    queryset = Properties.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        if self.request.method == 'PUT':
            self.permission_classes = [IsOwner()]
        return super().get_permissions()

    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))
        obj.views += 1
        obj.save()
        return obj

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Status.ARCHIVED.value
        instance.save()
        # TODO: add deletion tasks
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'Property has been archived and will be deleted in 30 days'})


class PropertiesRecommendationView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SmallPropertiesSerializer
    queryset = Properties.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))

    @staticmethod
    def asc_desc(queryset, price):
        print(queryset.filter(price__lte=price))
        print(queryset.filter(price__gte=price))
        return queryset.filter(price__gte=price).order_by('price'), queryset.filter(price__lte=price).order_by('-price')

    def get_queryset(self):
        obj = self.get_object()
        queryset = self.queryset.exclude(pk=obj.pk)
        queryset = queryset.filter(
            is_available=True,
            accommodation_type=obj.accommodation_type,
            flat_type=obj.flat_type,
            hotel_type=obj.hotel_type,
            room_type=obj.room_type,
            unique_type=obj.unique_type,
            house_type=obj.house_type,
            # rent_type=obj.rent_type,
        )
        q_same_price = queryset.filter(price=obj.price)
        q_asc_price, q_desc_price = self.asc_desc(queryset, obj.price)
        sorted_query = q_same_price.union(q_asc_price, q_desc_price)
        return sorted_query


class PropertyOrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    # filterset_class = PropertyOrderFilterSet

    def get_queryset(self):
        queryset = Orders.objects.filter(wallet_to__user=self.request.user)
        orders = self.request.query_params.get('filter', '')
        if orders == 'upcoming':
            queryset = queryset.filter(order_to__gte=timezone.now())
        elif orders == 'past':
            queryset = queryset.filter(order_to__lte=timezone.now())
        elif orders == 'cancelled':
            cancel_statuses = [TransactionStatus.CANCELLED_BY_CUSTOMER.value,
                               TransactionStatus.CANCELLED_BY_OWNER.value]
            queryset = queryset.filter(status__in=cancel_statuses)
        return queryset.order_by('-id')


class PropertyCancelView(APIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        self.serializer_class().cancel(instance)
        return Response(status=status.HTTP_200_OK)


class PropertiesArchiveView(APIView):
    serializer_class = PropertiesSerializer

    def get_object(self):
        return get_object_or_404(Properties, pk=self.kwargs.get('pk'), user=self.request.user)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Status.ARCHIVED.value
        instance.save()
        return Response(status=status.HTTP_200_OK, data=PropertiesSerializer(instance).data)


class AmenitiesListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()


class AmenitiesRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))


class PropertyOccupationView(generics.ListAPIView):
    serializer_class = OrderSerializer
    # filterset_class = PropertyOccupationsFilterSet

    def get_queryset(self):
        queryset = Orders.objects.filter(wallet_to__user=self.request.user)
        occupations = self.request.query_params.get('filter', '')
        if occupations == 'upcoming':
            queryset = queryset.filter(order_to__gte=timezone.now())
        elif occupations == 'past':
            queryset = queryset.filter(order_to__lte=timezone.now())
        elif occupations == 'cancelled':
            cancel_statuses = [TransactionStatus.CANCELLED_BY_CUSTOMER.value,
                               TransactionStatus.CANCELLED_BY_OWNER.value]
            queryset = queryset.filter(status__in=cancel_statuses)
        return queryset.order_by('-id')


class PropertiesPromotionView(generics.ListCreateAPIView):
    serializer_class = PropertiesPromotionSerializer

    def get_queryset(self):
        return PromotionObjects.objects.filter(user=self.request.user)
