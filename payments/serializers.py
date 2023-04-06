import datetime

from django.db.models import F
from rest_framework import serializers

from payments.enums import TransactionStatus
from payments.models import Orders, Wallet, CancelMultiplier
from properties.models import Properties
from properties.serializers import SmallPropertiesSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = [
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
            'payments',
        ]
        read_only_fields = [
            'pk',
            'wallet_from',
            'wallet_to',
            'property',
            'amount',
            'safe_amount',
            'payments',
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)

        try:
            property = Properties.objects.get(pk=self.context['request'].parser_context['kwargs']['pk'])
        except Properties.DoesNotExist:
            raise serializers.ValidationError({'property': 'Property does not exist'})

        attrs['property'] = property
        attrs['wallet_from'] = self.context['request'].user.wallet
        attrs['wallet_to'] = property.user.wallet
        attrs['amount'] = property.price
        attrs['safe_amount'] = getattr(property, 'safe_amount', 0)

        if attrs['wallet_from'] == attrs['wallet_to']:
            raise serializers.ValidationError('You can not transfer money to yourself')

        return attrs

    def cancel(self, instance):
        instance.status = self.validated_data.get('status')
        instance.rejected_type = self.validated_data.get('rejected_type')
        instance.rejected_reason = self.validated_data.get('rejected_reason')
        instance.save()
        if instance.order_from - datetime.datetime.now() >= datetime.timedelta(hours=168):
            Wallet.objects.get(pk=instance.wallet_from.pk).update(
                amount=F('amount') + instance.amount * CancelMultiplier.objects.get(pk=1).amount_168)
        elif instance.order_from - datetime.datetime.now() >= datetime.timedelta(hours=72):
            Wallet.objects.get(pk=instance.wallet_from.pk).update(
                amount=F('amount') + instance.safe_amount * CancelMultiplier.objects.get(pk=1).amount_72)
        elif instance.order_from - datetime.datetime.now() >= datetime.timedelta(hours=24):
            Wallet.objects.get(pk=instance.wallet_from.pk).update(
                amount=F('amount') + instance.safe_amount * CancelMultiplier.objects.get(pk=1).amount_24)
        elif instance.order_from - datetime.datetime.now() < datetime.timedelta(hours=24):
            Wallet.objects.get(pk=instance.wallet_from.pk).update(
                amount=F('amount') + instance.safe_amount * CancelMultiplier.objects.get(pk=1).amount_0)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['property'] = SmallPropertiesSerializer(instance.property).data
        return rep
