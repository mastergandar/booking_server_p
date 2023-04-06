from django.db import models
from django.utils.translation import gettext_lazy as _


class TransactionStatus(models.IntegerChoices):
    PENDING = 0, _('Pending')
    COMPLETE = 1, _('Complete')
    CANCELLED_BY_CUSTOMER = 2, _('Cancelled by customer')
    CANCELLED_BY_OWNER = 3, _('Cancelled by owner')


class RejectedType(models.IntegerChoices):
    CHANGED_YOUR_MIND = 0, _('Changed your mind')
    FOUND_ANOTHER_PLACE_TO_LIVE = 1, _('Found another place to live')
    CHANGED_THE_ROUTE = 2, _('Changed the route')
    CIRCUMSTANCES_HAVE_CHANGED = 3, _('Circumstances have changed')
    ANOTHER_REASON = 4, _('Another reason')
    PROPERTY_OWNER_CHANGED_TERMS = 5, _('Property owner changed terms')


class Badge(models.IntegerChoices):
    NEW = 0, _('New')
    POPULAR = 1, _('Popular')
    TOP = 2, _('Top')
