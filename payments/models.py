from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction

from payments.enums import TransactionStatus, RejectedType, Badge


class Wallet(models.Model):

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="Wallet"
    )

    amount = models.IntegerField(
        'Amount',
        default=0,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f'Wallet {self.user.email if self.user.email else self.user.id}'


class Orders(models.Model):

    wallet_from = models.ForeignKey(
        'Wallet',
        on_delete=models.CASCADE,
        related_name="transaction_out"
    )

    wallet_to = models.ForeignKey(
        'Wallet',
        on_delete=models.CASCADE,
        related_name="transaction_in"
    )

    property = models.ForeignKey(
        'properties.Properties',
        on_delete=models.CASCADE,
        related_name="transaction"
    )

    amount = models.DecimalField(
        'Amount',
        null=False,
        blank=False,
        max_digits=10,
        decimal_places=2,
    )

    safe_amount = models.DecimalField(
        'Safe amount',
        null=False,
        blank=False,
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.SmallIntegerField(
        'Status',
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING.value
    )

    rejected_type = models.SmallIntegerField(
        'Rejected type',
        choices=RejectedType.choices,
        null=True,
        blank=True
    )

    rejected_reason = models.CharField(
        'Rejected reason',
        max_length=250,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    order_from = models.DateTimeField(
        null=True,
        blank=True
    )

    order_to = models.DateTimeField(
        null=True,
        blank=True
    )

    payments = models.ForeignKey(
        'payments.Payments',
        on_delete=models.CASCADE,
        related_name="payments",
        null=True
    )

    def __str__(self):
        return f'Order {self.id}'

    @transaction.atomic
    def do_transfer(self):
        self.wallet_from.amount -= self.amount
        self.wallet_from.save()
        self.wallet_to.amount += self.amount
        self.wallet_to.save()


class Payments(models.Model):

    amount = models.IntegerField(
        'Amount',
        null=True,
        blank=True
    )

    receipt_number = models.CharField(
        'MpesaReceiptNumber',
        max_length=20,
        null=True,
        blank=True
    )

    transaction_date = models.DateTimeField(
        auto_now_add=False,
        editable=False,
        null=True,
        blank=True
    )

    phone_number = models.IntegerField(
        'PhoneNumber',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Payment {self.id}'


class Withdraw(models.Model):

    wallet_from = models.ForeignKey(
        'Wallet',
        on_delete=models.CASCADE,
        related_name="Wallet"
    )

    amount = models.IntegerField(
        'Amount',
        blank=False,
        null=False,
        validators=[MinValueValidator(1)]
    )

    card = models.IntegerField(
        'Card number',
        blank=False,
        null=False
    )

    def __str__(self):
        return f'Withdraw {self.id}'


class CompanyBalance(models.Model):

    amount = models.IntegerField(
        'Amount',
        default=0,
        validators=[MinValueValidator(0)]
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    def __str__(self):
        return f'Balance: {self.amount if self.amount else self.id}'


class Fee(models.Model):

    version = models.IntegerField(
        'Version',
        default=1
    )

    is_main = models.BooleanField(
        'Is main',
        default=False
    )

    amount = models.IntegerField(
        'Amount',
        default=0,
        validators=[MinValueValidator(0)]
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    def __str__(self):
        return f'Fee: {self.amount if self.amount else self.id}'


class CancelMultiplier(models.Model):

    amount_168 = models.FloatField(
        'Amount 168h+',
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    amount_72 = models.FloatField(
        'Amount 168h-72h',
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    amount_24 = models.FloatField(
        'Amount 72h-24h',
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    amount_0 = models.FloatField(
        'Amount last 24h',
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    def __str__(self):
        return 'Cancel multiplier'


class Promotion(models.Model):

    amount = models.IntegerField(
        'Amount',
        default=0,
        validators=[MinValueValidator(0)]
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    def __str__(self):
        return f'Promotion: {self.amount if self.amount else self.id}'


class PromotionObjects(models.Model):

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="PromotionObjects",
        null=True,
        blank=True
    )

    promotion = models.ForeignKey(
        'Promotion',
        on_delete=models.CASCADE,
        related_name="PromotionObjects"
    )

    property = models.ForeignKey(
        'properties.Properties',
        on_delete=models.CASCADE,
        related_name="PromotionObjects"
    )

    badge = models.SmallIntegerField(
        'Badge',
        choices=Badge.choices,
        default=Badge.NEW.value
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    def __str__(self):
        return f'Promotion: {self.promotion.amount if self.promotion.amount else self.id}'
