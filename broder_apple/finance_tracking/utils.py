from .models import Account
from django.conf import settings


def create_predefined_accounts():
    predefined_accounts = settings.PREDEFINED_ACCOUNTS

    print(predefined_accounts)
    for account in predefined_accounts:
        account_id = account["id"]
        name = account["name"]
        nature = account["nature"]

        if not Account.objects.filter(id=account_id).exists():
            Account.objects.create(id=account_id, name=name, nature=nature)
            print(f"Created account: {name} with ID: {account_id}")
        else:
            print(f"Account already exists: {name} with ID: {account_id}")
