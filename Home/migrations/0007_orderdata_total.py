# Generated by Django 2.2 on 2019-05-18 19:35

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0006_positioninmenu_counttmp'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdata',
            name='total',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6),
        ),
    ]
