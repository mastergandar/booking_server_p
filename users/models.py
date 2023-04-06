from enum import Enum

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator, EmailValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models, transaction

from core.file_storage import avatar_property_avatar_path
from core.validators import validate_phone_simple, validate_avatar_max_size
from payments.models import Wallet


class UserStatuses(Enum):
    ACTIVE = 0
    HARD_BANNED = 1


class UserQuerySet(models.QuerySet):
    def get_by_email(self, raw_login: str) -> 'User':
        return self.get(email=raw_login)

    def get_verified(self) -> 'User':
        return self.get(is_verified=True)

    def get_not_verified(self) -> 'User':
        return self.get(is_verified=False)

    def get_not_banned(self):
        return self.filter(status=UserStatuses.ACTIVE.value)


class UserManager(BaseUserManager):

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def normalize_email(self, email_address):
        """
        Normalize the email address by lowercasing the domain part of it.
        """

        email_address = email_address or ''
        try:
            email_name, domain_part = email_address.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email_address = email_name.lower() + '@' + domain_part.lower()
        return email_address

    def _create_user(self, email: str, password: str, **extra_fields) -> 'User':
        with transaction.atomic():
            if not email:
                raise ValueError('Users must have an email address')
            if not password:
                raise ValueError('Users must have a password')
            extra_fields.setdefault('is_staff', False)
            extra_fields.setdefault('is_superuser', False)
            user = self.model(email=self.normalize_email(email), **extra_fields)
            user.set_password(password)
            user.activation_email_code = User.objects.make_random_password(length=32)
            user.save()
        return user

    def create_user(
                    self,
                    email: str,
                    password: str,
                    username: str = '',
                    is_email_active: bool = False
                    ) -> 'User':
        user = self._create_user(
            email=email,
            password=password,
            username=username,
            is_email_active=is_email_active
        )
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        email = 'root@roompesa.com'

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    class Meta:
        ordering = ['email']

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    STATUSES = [
        (UserStatuses.ACTIVE.value, 'Active'),
        (UserStatuses.HARD_BANNED.value, 'Baned')
    ]

    # common user info
    username = models.CharField(
        verbose_name=_('User name'),
        max_length=250,
        null=True,
        blank=True,
        validators=[MinLengthValidator(1)]
    )
    password = models.CharField(verbose_name=_('Password'), max_length=254, blank=False, null=False)
    avatar = models.ImageField(
        verbose_name=_("Avatar image"),
        upload_to=avatar_property_avatar_path,
        validators=[validate_avatar_max_size],
        null=True,
        blank=True
    )
    status = models.PositiveSmallIntegerField(
        _('Status'),
        choices=STATUSES,
        default=UserStatuses.ACTIVE.value
    )

    # Contacts
    phone_number = models.CharField(
        verbose_name=_('Phone number'),
        validators=[validate_phone_simple],
        max_length=18,
        null=True,
        blank=True
    )
    email = models.CharField(
        _('Email'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator(), EmailValidator()],
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    activation_email_code = models.CharField(
        max_length=32,
        verbose_name=_('Email confirmation code'),
        null=True, blank=True
    )
    email_activation_date = models.DateTimeField(blank=True, null=True)
    is_email_active = models.BooleanField('Email confirmed', default=False)

    # Detail info
    bio = models.TextField(
        max_length=4000,
        null=True,
        blank=True
    )
    rating = models.FloatField(
        'Rating',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(
        'Verified',
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return f"User: {self.email if self.email else self.id}"

    @property
    def wallet(self):
        wallet = Wallet.objects.get(user=self)
        return wallet

    def confirm_email(self):
        self.is_email_active = True
        self.activation_email_code = None
        self.email_activation_date = timezone.now()
