from django.db import models
from django.utils.translation import gettext_lazy as _


class ReportType(models.IntegerChoices):
    THE_AD_IS_NOT_RELEVANT = 0, _('The ad is not relevant')
    INCORRECT_DATA = 1, _('Incorrect data')
    MISLEADING_PRICE_OR_TERMS = 2, _('Misleading price or terms')
    THIS_IS_NOT_REAL_HOUSING = 3, _('This is not real housing')
    THIS_IS_A_SCAM = 4, _('This is a scam')
    CONTAINS_OFFENSIVE_MATERIALS = 5, _('Contains offensive materials')
    OTHER = 6, _('Other')


class ReportStatus(models.IntegerChoices):
    NEW = 0, _('New')
    IN_PROGRESS = 1, _('In progress')
    RESOLVED = 2, _('Resolved')
    REJECTED = 3, _('Rejected')


class NotifyCode(models.IntegerChoices):
    NEW_USER_GREETING = 1, 'New user greeting'

    PROPERTY_CREATED_AND_AWAITING_APPROVAL = 2, 'Property created. Awaiting approval'
    PROPERTY_STATUS_CHANGED = 3, 'Property status changed'
    NEW_REVIEW_IN_YOUR_PROPERTY = 4, 'New review in your property'

    PROPERTY_PAID = 5, 'Property paid'
    PROPERTY_ARRIVAL_TIMEOUT = 6, 'Arrival time is ending'
    WITHDRAW_REQUEST_PLACED = 7, 'Withdraw request placed'

    WITHDRAW_REQUEST_COMPLETE = 8, 'Withdraw request complete'
    PROPERTY_VIEWED = 9, 'Property viewed'
    PROPERTY_DISCOUNT = 10, 'Property discount'

    REPORT_RESOLVED = 11, 'Report resolved'
    REPORT_REJECTED = 12, 'Report rejected'
