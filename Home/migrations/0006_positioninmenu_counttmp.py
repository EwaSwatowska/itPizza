# Generated by Django 2.2 on 2019-05-15 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_orderdata_orderposition'),
    ]

    operations = [
        migrations.AddField(
            model_name='positioninmenu',
            name='countTmp',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=4),
        ),
    ]