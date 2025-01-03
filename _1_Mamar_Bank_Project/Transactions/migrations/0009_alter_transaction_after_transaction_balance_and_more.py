# Generated by Django 5.1.2 on 2024-11-22 14:46

import Transactions.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transactions', '0008_b2b'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='after_transaction_balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default=Transactions.models.generate_transaction_id, editable=False, max_length=15),
        ),
    ]
