# Generated by Django 5.1.1 on 2024-10-27 19:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "finance_tracking",
            "0004_alter_bookentry_account_alter_bookentry_transaction_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraccountbalance",
            name="balance",
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
