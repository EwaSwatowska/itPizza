from datetime import date, datetime
from django.db import models
from decimal import *
from django.utils import timezone

# Create your models here.

class Pizza(models.Model):
    name = models.CharField(max_length=20)
    ingredients = models.CharField(max_length=150)
    looseOfPrice = models.DecimalField(decimal_places=2, max_digits=6, default=0)

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
    # w pizza_FK jest nazwa pizzy, składniki
    Pizza_FK = models.ForeignKey(
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
    nameAndSurname  = models.CharField(max_length=60)
    street          = models.CharField(max_length=40)
    streetNumber    = models.CharField(max_length=5)
    houseNumber     = models.CharField(max_length=5)
    email           = models.CharField(max_length=30)
    phoneNumber     = models.DecimalField(decimal_places=0, max_digits=9)
    total           = models.DecimalField(decimal_places=2, max_digits=6, default = Decimal('0.00'))
    date            = models.DateTimeField(auto_now_add=True)
    # to musi byc pole wyliczalne
    pizzeria        = models.ForeignKey(
        'Pizzeria',
        on_delete=models.CASCADE,
    )
    DRINKS = (
        ('1', 'Pepsi'),
        ('2', 'Coca Cola'),
        ('3', 'Sprite'),
        ('4', 'Sok pomarańczowy'),
        ('5', 'Woda'),
        ('6', 'Bez napoju'),
    )
    drink           = models.CharField(max_length=1, choices=DRINKS, default='6')
    numberOfDrinks  = models.IntegerField(default=0)
    SAUCES = (
        ('1', 'Sos pomidorowy'),
        ('2', 'Sos czosnkowy'),
        ('3', 'Sos BBQ'),
        ('4', 'Sos orientalny'),
        ('5', 'Sos tysiąca wysp'),
        ('6', 'Bez sosu'),
    )
    sauce           = models.CharField(max_length=1, choices=SAUCES, default='6')
    numberOfSauces  = models.IntegerField(default=0)
    #to potrzebne do sprawdzania zamówień danej pizzerii
    orderNumber     = models.BigIntegerField(default=0)
    PAYMETHODS = (
        ('1', 'Gotówka (przy odbiorze)'),
        ('2', 'Karta płatnicza'),
        ('3', 'Przelew'),
    )
    pay             = models.CharField(max_length=1, choices=PAYMETHODS, default='1')
    Coupon_FK = models.ForeignKey(
        'Coupon',
        blank=True, null=True,
        on_delete=models.CASCADE,
    )
    ORDER_STATUS = (
        ('1', 'Zamówienie przyjęte'),
        ('2', 'Zamówienie w trakcie przygotowania'),
        ('3', 'Zamówienie jest pakowane'),
        ('4', 'Zamówienie w dowozie'),
        ('5', 'Zamówienie zakończone'),
        ('6', 'Zamówienie usunięte z bazy'),
    )
    # w Pizza_FK jest nazwa pizzy, składniki
    orderStatus = models.CharField(max_length=1, choices=ORDER_STATUS, default='1')



# ------------------- Dane zamowienia - jakie produkty i dla kogo -------------------

class OrderPosition(models.Model):
    order_id = models.ForeignKey(
        'OrderData',
        on_delete=models.CASCADE,
    )
    positionInMenu_id = models.ForeignKey(
        'PositionInMenu',
        on_delete=models.CASCADE,
    )
    numberOfPIM = models.IntegerField(default=0) #liczba (position in menu) danych pozycji w menu, tych zamowionych

class Coupon(models.Model):
    code = models.CharField(max_length=5)
    discount = models.IntegerField(default=5)
    numberOfCoupons = models.IntegerField(default=1)

    def __str__(self):
        return self.code

