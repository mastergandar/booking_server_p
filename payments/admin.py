from django.contrib import admin

from payments.models import CancelMultiplier, Fee, Orders


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'version', 'is_main', 'amount', 'updated_at')
    list_filter = ('version', 'is_main', 'updated_at')
    search_fields = ('version', 'amount', 'updated_at')
    ordering = ('-updated_at',)


@admin.register(CancelMultiplier)
class CancelMultiplierAdmin(admin.ModelAdmin):
    list_display = ('pk', 'amount_168', 'amount_72', 'amount_24', 'amount_0', 'updated_at')
    fields = ('amount_168', 'amount_72', 'amount_24', 'amount_0', 'updated_at')
    readonly_fields = ('updated_at',)
    ordering = ('-updated_at',)


@admin.register(Orders)
class Orders(admin.ModelAdmin):
    list_display = (
        'pk',
        'wallet_from',
        'wallet_to',
        'property',
        'amount',
        'safe_amount',
        'status',
        'rejected_type',
        'rejected_reason',
        'created_at',
        'order_from',
        'order_to',
        'payments'
    )
    list_filter = (
        'wallet_from',
        'wallet_to',
        'property',
        'amount',
        'safe_amount',
        'status',
        'rejected_type',
        'rejected_reason',
        'created_at',
        'order_from',
        'order_to',
        'payments'
    )
    search_fields = ('wallet_from', 'wallet_to', 'property', 'amount', 'safe_amount', 'status', 'rejected_type', 'rejected_reason', 'created_at', 'order_from', 'order_to', 'payments')
    ordering = ('-created_at',)
