from django.db import models
from django.utils.translation import gettext_lazy as _


class AccommodationType(models.IntegerChoices):
    HOUSE = 0, _('House')
    FLAT = 1, _('Flat')
    ROOM = 2, _('Room')
    UNIQUE = 3, _('Unique')
    HOTEL = 4, _('Hotel')


class FlatType(models.IntegerChoices):
    ATELIER = 0, _('Atelier')
    APARTMENT = 1, _('Apartment')
    LOFT = 2, _('Loft')


class HouseType(models.IntegerChoices):
    HOUSE = 0, _('House')
    COUNTRY_HOUSE = 1, _('Country house')
    COTTAGE = 2, _('Cottage')
    TOWNHOUSE = 3, _('Townhouse')


class RoomType(models.IntegerChoices):
    RWA = 0, _('Room with amenities')
    RIA = 1, _('Room in apartment')
    BED = 2, _('Bed in common room')


class UniqueType(models.IntegerChoices):
    TRANSPORT = 0, _('Transport')
    NATURAL = 1, _('Natural')
    TOWER = 2, _('Tower')
    OTHER = 3, _('Other')


class HotelType(models.IntegerChoices):
    HOTEL = 0, _('Hotel')
    HOSTEL = 1, _('Hostel')
    RESORT = 2, _('Resort')
    BAB = 3, _('B&B')
    APART = 4, _('Apart-hotel')


class RentType(models.IntegerChoices):
    INDIVIDUAL = 0, _('Individual')
    COMPANY = 1, _('Company')


class Status(models.IntegerChoices):
    PUBLISHED = 0, _('Published')
    ARCHIVED = 1, _('Archived')
    DRAFT = 2, _('Draft')

