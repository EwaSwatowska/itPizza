# Generated by Django 2.2 on 2019-05-27 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0013_auto_20190527_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdata',
            name='orderStatus',
            field=models.CharField(choices=[('1', 'Zamówienie przyjęte'), ('2', 'Zamówienie w trakcie przygotowania'), ('3', 'Zamówienie jest pakowane'), ('4', 'Zamówienie w dowozie'), ('5', 'Zamówienie zakończone')], default='1', max_length=1),
        ),
    ]