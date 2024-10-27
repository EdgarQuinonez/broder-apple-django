# signals.py
from django.conf import settings
from django.db.models.signals import post_migrate, post_save, post_delete
from django.dispatch import receiver
from .models import Account, BookEntry


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


@receiver(post_save, sender=BookEntry)
def adjust_balance_on_create(sender, instance, created, **kwargs):
    if created:
        user_account_balance = instance.user_account_balance

        if instance.account.nature in [Account.ASSET, Account.EXPENSE]:
            if instance.balance_type == BookEntry.DEBIT:
                user_account_balance.balance += instance.amount
            else:
                user_account_balance.balance -= instance.amount
        elif instance.account.nature in [
            Account.LIABILITY,
            Account.EQUITY,
            Account.REVENUE,
        ]:
            if instance.balance_type == BookEntry.CREDIT:
                user_account_balance.balance += instance.amount
            else:
                user_account_balance.balance -= instance.amount

        user_account_balance.save()


@receiver(post_delete, sender=BookEntry)
def revert_balance_on_delete(sender, instance, **kwargs):
    user_account_balance = instance.user_account_balance

    if instance.account.nature in [Account.ASSET, Account.EXPENSE]:
        if instance.balance_type == BookEntry.DEBIT:
            user_account_balance.balance -= instance.amount
        else:
            user_account_balance.balance += instance.amount
    elif instance.account.nature in [
        Account.LIABILITY,
        Account.EQUITY,
        Account.REVENUE,
    ]:
        if instance.balance_type == BookEntry.CREDIT:
            user_account_balance.balance -= instance.amount
        else:
            user_account_balance.balance += instance.amount

    user_account_balance.save()
