# Generated by Django 2.2 on 2019-05-18 19:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0007_orderdata_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdata',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
