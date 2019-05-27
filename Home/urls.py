from django.urls import path
from . import views


urlpatterns = [
    # path('Home/', views.Home, name='itPizza home'),
    path('', views.Home, name='itPizza home'),
    #wywołanie funkcji Home z views.py, '' oznacza że nie ma nic po slashu w adresie URL
    path('oProjekcie/', views.oProjekcie, name='O projekcie'),
    path('Menu/', views.Menu, name='Menu'),
    path('SelectPizzeria/', views.SelectPizzeria, name='SelectPizzeria'),
    path('OrderList/', views.OrderList, name='OrderList'),
    path('OrderHead/', views.OrderHead, name='OrderHead'),
    path('OrderPlaced/', views.OrderPlaced, name='OrderPlaced'),
    path('CheckStatus/', views.CheckStatus, name='CheckStatus'),
]
