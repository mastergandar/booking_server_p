from django.db.models import F, Q
from django.utils import timezone
from django_filters import CharFilter, NumberFilter
from django_filters.rest_framework import FilterSet
from rest_framework.filters import OrderingFilter

from payments.enums import TransactionStatus
from payments.models import Orders
from properties.models import Properties


class PropertiesFilterSet(FilterSet):
    accommodation_type = CharFilter(method="filter_by_accommodation_type")
    flat_type = CharFilter(method="filter_by_flat_type")
    house_type = CharFilter(method="filter_by_house_type")
    room_type = CharFilter(method="filter_by_room_type")
    unique_type = CharFilter(method="filter_by_unique_type")
    hotel_type = CharFilter(method="filter_by_hotel_type")
    rent_type = CharFilter(method="filter_by_rent_type")
    guests_count = NumberFilter(method="filter_by_guests_count")
    bedrooms_count = NumberFilter(method="filter_by_bedrooms_count")
    beds_count = NumberFilter(method="filter_by_beds_count")
    bathrooms_count = NumberFilter(method="filter_by_bathrooms_count")
    amenities = CharFilter(method="filter_by_amenities")
    rules = CharFilter(method="filter_by_rules")
    time = CharFilter(method="filter_by_time")

    class Meta:
        model = Properties
        fields = [
            'user',
            'is_available',
        ]

    def combo_filter(self, queryset, name, combo_list: dict):

        if combo_list:
            print("PRE-MIDDLE", queryset)
            kwargs = {
                'guests_count__gte': combo_list.get('guests_count', 0),
                'bedrooms_count__gte': combo_list.get('bedrooms_count', 0),
                'beds_count__gte': combo_list.get('beds_count', 0),
                'bathrooms_count__gte': combo_list.get('bathrooms_count', 0),
            }
            if combo_list['accommodation_list']:
                queryset_accommodation = queryset.filter(
                    accommodation_type__in=combo_list['accommodation_list'], **kwargs
                )
            else:
                queryset_accommodation = queryset.none()
            print("queryset_accommodation", queryset_accommodation)
            if combo_list['flat_list']:
                queryset_flat = queryset.filter(flat_type__in=combo_list['flat_list'], **kwargs)
            else:
                queryset_flat = queryset.none()
            print("FLAT", queryset_flat)
            if combo_list['house_list']:
                queryset_house = queryset.filter(house_type__in=combo_list['house_list'], **kwargs)
            else:
                queryset_house = queryset.none()
            print("HOUSE", queryset_house)
            if combo_list['room_list']:
                queryset_room = queryset.filter(room_type__in=combo_list['room_list'], **kwargs)
            else:
                queryset_room = queryset.none()
            print("ROOM", queryset_room)
            if combo_list['unique_list']:
                queryset_unique = queryset.filter(unique_type__in=combo_list['unique_list'], **kwargs)
            else:
                queryset_unique = queryset.none()
            print("UNIQUE", queryset_unique)
            if combo_list['hotel_list']:
                queryset_hotel = queryset.filter(hotel_type__in=combo_list['hotel_list'], **kwargs)
            else:
                queryset_hotel = queryset.none()
            print("HOTEL", queryset_hotel)
            if combo_list['rent_list']:
                queryset_rent = queryset.filter(rent_type__in=combo_list['rent_list'], **kwargs)
            else:
                queryset_rent = queryset.none()
            print("RENT", queryset_rent)
            queryset = queryset_accommodation.union(
                queryset_flat, queryset_house, queryset_room, queryset_unique, queryset_hotel, queryset_rent
            )
            print("END QUERYSET", queryset)
        return queryset.order_by('-id')

    def filter_by_accommodation_type(self, queryset, name, accommodation_list: str):

        if accommodation_list:
            type_list = [int(i) for i in accommodation_list.split(',')]
            queryset = queryset.filter(accommodation_type__in=type_list)

        return queryset.order_by('-id')

    def filter_by_flat_type(self, queryset, name, flat_list: str):

        if flat_list:
            type_list = [int(i) for i in flat_list.split(',')]
            queryset = queryset.filter(flat_type__in=type_list)

        return queryset.order_by('-id')

    def filter_by_house_type(self, queryset, name, house_list: str):

            if house_list:
                type_list = [int(i) for i in house_list.split(',')]
                queryset = queryset.filter(house_type__in=type_list)

            return queryset.order_by('-id')

    def filter_by_room_type(self, queryset, name, room_list: str):

        if room_list:
            type_list = [int(i) for i in room_list.split(',')]
            queryset = queryset.filter(room_type__in=type_list)

        return queryset.order_by('-id')

    def filter_by_unique_type(self, queryset, name, unique_list: str):

        if unique_list:
            type_list = [int(i) for i in unique_list.split(',')]
            queryset = queryset.filter(unique_type__in=type_list)

        return queryset.order_by('-id')

    def filter_by_hotel_type(self, queryset, name, hotel_list: str):

        if hotel_list:
            type_list = [int(i) for i in hotel_list.split(',')]
            queryset = queryset.filter(hotel_type__in=type_list)

        return queryset.order_by('-id')

    def filter_by_rent_type(self, queryset, name, rent_list: str):

        if rent_list:
            type_list = [int(i) for i in rent_list.split(',')]
            queryset = queryset.filter(rent_type__in=type_list)

        return queryset.order_by('-id')

    def filter_by_guests_count(self, queryset, name, guests_count: int):

        if guests_count:
            queryset = queryset.filter(guests_count__gte=guests_count)

        return queryset.order_by('-id')

    def filter_by_bedrooms_count(self, queryset, name, bedrooms_count: int):

        if bedrooms_count:
            queryset = queryset.filter(bedrooms_count__gte=bedrooms_count)

        return queryset.order_by('-id')

    def filter_by_beds_count(self, queryset, name, beds_count: int):

        if beds_count:
            queryset = queryset.filter(beds_count__gte=beds_count)

        return queryset.order_by('-id')

    def filter_by_bathrooms_count(self, queryset, name, bathrooms_count: int):

        if bathrooms_count:
            queryset = queryset.filter(bathrooms_count__gte=bathrooms_count)

        return queryset.order_by('-id')

    def filter_by_amenities(self, queryset, name, amenities_list: str):

        if amenities_list:
            amenities_list = [int(i) for i in amenities_list.split(',')]
            queryset = queryset.filter(amenities__amenity__in=amenities_list)

        return queryset.order_by('-id')

    def filter_by_rules(self, queryset, name, rules_list: str):

            if rules_list:
                rules_list = [int(i) for i in rules_list.split(',')]
                queryset = queryset.filter(rules__pk__in=rules_list)

            return queryset.order_by('-id')

    def filter_by_time(self, queryset, name, time: str):
        if time:
            queryset = queryset.filter(time__gte=time)

        return queryset.order_by('-id')


class NullsAlwaysLastOrderingFilter(OrderingFilter):
    """ Use Django 1.11 nulls_last feature to force nulls to bottom in all orderings. """

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            f_ordering = []
            for o in ordering:
                if not o:
                    continue
                if o[0] == '-':
                    f_ordering.append(F(o[1:]).desc(nulls_last=True))
                else:
                    f_ordering.append(F(o).asc(nulls_last=True))

            return queryset.order_by(*f_ordering)

        return queryset


class PropertyOrderFilterSet(FilterSet):

    filters = CharFilter(method="filter_by_my_orders")

    class Meta:
        model = Orders
        fields = [
            'wallet_to',
            'wallet_from',
            'status',
        ]

    def filter_by_my_orders(self, queryset, name, my_orders: str):
        if my_orders == 'upcoming':
            queryset = queryset.filter(wallet_from__user=self.request.user, order_to__gte=timezone.now())
        elif my_orders == 'past':
            queryset = queryset.filter(wallet_from__user=self.request.user, order_to__lte=timezone.now())
        elif my_orders == 'cancelled':
            cancel_statuses = [TransactionStatus.CANCELLED_BY_CUSTOMER.value,
                               TransactionStatus.CANCELLED_BY_OWNER.value]
            queryset = queryset.filter(wallet_from__user=self.request.user, status__in=cancel_statuses)
        return queryset.order_by('-id')


class PropertyOccupationsFilterSet(FilterSet):

    filters = CharFilter(method="filter_by_occupations")

    class Meta:
        model = Orders
        fields = [
            'wallet_to',
            'wallet_from',
            'status',
        ]

    def filter_by_occupations(self, queryset, name, occupations: str):
        if occupations == 'upcoming':
            queryset = queryset.filter(wallet_to__user=self.request.user, order_to__gte=timezone.now())
        elif occupations == 'past':
            queryset = queryset.filter(wallet_to__user=self.request.user, order_to__lte=timezone.now())
        elif occupations == 'cancelled':
            cancel_statuses = [TransactionStatus.CANCELLED_BY_CUSTOMER.value,
                               TransactionStatus.CANCELLED_BY_OWNER.value]
            queryset = queryset.filter(wallet_to__user=self.request.user, status__in=cancel_statuses)
        return queryset.order_by('-id')
