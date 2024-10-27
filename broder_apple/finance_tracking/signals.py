# signals.py
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Account


@receiver(post_migrate)
def create_predefined_accounts(sender, **kwargs):
    predefined_accounts = getattr(settings, "PREDEFINED_ACCOUNTS", [])

    for account_data in predefined_accounts:
        Account.objects.get_or_create(
            id=account_data["id"],
            defaults={
                "name": account_data["name"],
                "nature": account_data["nature"],
            },
        )
