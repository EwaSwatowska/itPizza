from datetime import date, datetime
from django.db import models
from decimal import *
from django.utils import timezone

# Create your models here.

class Pizza(models.Model):
    name = models.CharField(max_length=20)
    ingredients = models.CharField(max_length=150)

    def __str__(self):
        return self.name + "  -----  " + self.ingredients

class Pizzeria(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=150)
    phoneNumber = models.DecimalField(decimal_places=0, max_digits=9)
    dateMenu = models.DateField(default=date.today)

    def __str__(self):
        return self.name

class PositionInMenu(models.Model):
    PIZZA_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('X', 'XXL'),
    )
    # w pizza_id jest nazwa pizzy, składniki
    pizza_id = models.ForeignKey(
        'Home.Pizza',
        on_delete=models.CASCADE,
    )
    pizzaSize = models.CharField(max_length=1, choices=PIZZA_SIZES)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    pizzeria_id = models.ForeignKey(
        'Home.Pizzeria',
        on_delete=models.CASCADE,
    )
    countTmp = models.DecimalField(decimal_places=0, max_digits=4, default=0) # pole pomocnicze do obsłig OrderList

# ----------------- Dane wprowadzone przez uzytkownika -----------------

class OrderData(models.Model):
    nameAndSurname = models.CharField(max_length=60)
    street = models.CharField(max_length=40)
    streetNumber    = models.CharField(max_length=5)
    houseNumber     = models.CharField(max_length=5)
    email           = models.CharField(max_length=30)
    phoneNumber     = models.DecimalField(decimal_places=0, max_digits=9)
    total           = models.DecimalField(decimal_places=2, max_digits=6, default = Decimal('0.00'))
    date            = models.DateTimeField(auto_now_add=True)
    # to musi byc pole wyliczalne
    pizzeria = models.ForeignKey(
        'Pizzeria',
        on_delete=models.CASCADE,
    )
    #to potrzebne do sprawdzania zamówień danej pizzerii


# ------------------- Dane zamowienia - jakie produkty i dla kogo -------------------

class OrderPosition(models.Model):
    positionInMenu_id = models.ForeignKey(
        'Pizza',
        on_delete=models.CASCADE,
    )
    order_id = models.ForeignKey(
        'OrderData',
        on_delete=models.CASCADE,
    )
