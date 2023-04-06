
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='users.User')
def create_user_wallet(sender, instance, created, raw=False, **kwargs):
    if created and not raw:
        model = apps.get_model('payments', 'Wallet')
        model.objects.create(user=instance)
