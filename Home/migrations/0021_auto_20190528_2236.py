# Generated by Django 2.2 on 2019-05-28 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0020_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdata',
            name='pay',
        ),
        migrations.AddField(
            model_name='orderdata',
            name='Coupon_FK',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Home.Coupon'),
        ),
    ]