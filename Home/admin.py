from django.contrib import admin

from .models import Pizza, Pizzeria, PositionInMenu, OrderData, OrderPosition

# Register your models here.

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ingredients')
    list_display_links = ('id', 'name', 'ingredients')
    list_filter = ('name', 'ingredients')

class PositionInMenuAdmin(admin.ModelAdmin):
    list_display = ('pizza_id', 'pizzaSize', 'price', 'pizzeria_id')
    list_display_links = ('pizza_id', 'pizzaSize', 'price', 'pizzeria_id')
    list_filter = ('pizza_id', 'pizzeria_id')

class OrderDataAdmin(admin.ModelAdmin):
    list_display = ('nameAndSurname', 'street', 'streetNumber', 'houseNumber', 'email', 'phoneNumber', 'total', 'date', 'pizzeria', 'orderNumber', 'orderStatus')

class OrderPositionAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'positionInMenu_id', 'numberOfPIM')

admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Pizzeria)
admin.site.register(PositionInMenu, PositionInMenuAdmin)
admin.site.register(OrderData, OrderDataAdmin)
admin.site.register(OrderPosition, OrderPositionAdmin)






