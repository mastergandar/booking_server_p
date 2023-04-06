from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from file_manager.models import LinkedImages
from social.enums import ReportType, ReportStatus, NotifyCode


class Review(models.Model):

    limit = models.Q(app_label='properties', model='properties') | \
            models.Q(app_label='users', model='user')

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='review',
        null=False,
        limit_choices_to=limit
    )
    object_id = models.BigIntegerField(null=False)
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="Review"
    )

    description = models.TextField(
        'Description',
        null=False,
        blank=False
    )

    purity = models.FloatField(
        'Rating',
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)]
    )

    location = models.FloatField(
        'Rating',
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)]
    )

    communication = models.FloatField(
        'Rating',
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)]
    )

    price_quality = models.FloatField(
        'Rating',
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)]
    )

    created_at = models.DateTimeField(
        'Created at',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Review #{self.id}'

    @property
    def images(self):
        images = LinkedImages.objects.filter(content_type=self.content_type, object_id=self.object_id)
        images_list = [image.image.url for image in images]
        return images_list


class Report(models.Model):
    limit = models.Q(app_label='properties', model='properties') | \
            models.Q(app_label='users', model='user')

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='report',
        null=False,
        limit_choices_to=limit
    )
    object_id = models.BigIntegerField(null=False)
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="Report"
    )

    description = models.TextField(
        'Description',
        null=False,
        blank=False
    )

    report_type = models.SmallIntegerField(
        'Report type',
        choices=ReportType.choices,
        null=False,
        blank=False
    )

    status = models.SmallIntegerField(
        'Status',
        choices=ReportStatus.choices,
        null=False,
        blank=False,
        default=ReportStatus.NEW.value
    )

    def __str__(self):
        return f'Report #{self.id}'

    @property
    def images(self):
        images = LinkedImages.objects.filter(content_type=self.content_type, object_id=self.object_id)
        images_list = [image.image.url for image in images]
        return images_list


class ReportMessages(models.Model):

    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="ReportMessages"
    )

    message = models.TextField(
        'Message',
        null=False,
        blank=False
    )

    created_at = models.DateTimeField(
        'Created at',
        auto_now_add=True,
    )


class NotifyQuerySet(models.QuerySet):

    def owner(self, user):
        return self.filter(user=user)


class NotifyManager(models.Manager):

    def get_queryset(self):
        return NotifyQuerySet(self.model, using=self._db).order_by('-created_at')


class Notify(models.Model):

    code = models.PositiveSmallIntegerField('code', choices=NotifyCode.choices)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifies')
    payload = models.JSONField('payload', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField('Is viewed', default=False)

    objects = NotifyManager()

    def __str__(self):
        return f'Notify #{self.id}'


class ReportList(Report):
    class Meta:
        proxy = True


class Favorite(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='favorites')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='favorites_type')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Favorite #{self.id}'

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    @property
    def obj(self):
        if self.content_type.model == 'properties':
            from properties.serializers import SmallPropertiesSerializer
            return SmallPropertiesSerializer(self.content_object).data
        return None
