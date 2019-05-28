from django.contrib import admin

from .models import Pizza, Pizzeria, PositionInMenu, OrderData, OrderPosition, Coupon

# Register your models here.

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ingredients', 'looseOfPrice')
    list_display_links = ('id', 'name', 'ingredients')
    list_filter = ('name', 'ingredients')

class PositionInMenuAdmin(admin.ModelAdmin):
    list_display = ('Pizza_FK', 'pizzaSize', 'price', 'pizzeria_id')
    list_display_links = ('Pizza_FK', 'pizzaSize', 'price', 'pizzeria_id')
    list_filter = ('Pizza_FK', 'pizzeria_id')

class OrderDataAdmin(admin.ModelAdmin):
    list_display = ('nameAndSurname', 'street', 'streetNumber', 'houseNumber', 'email', 'phoneNumber', 'total', 'date', 'pizzeria', 'orderNumber', 'orderStatus')

class OrderPositionAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'positionInMenu_id', 'numberOfPIM')

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'numberOfCoupons')

admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Pizzeria)
admin.site.register(PositionInMenu, PositionInMenuAdmin)
admin.site.register(OrderData, OrderDataAdmin)
admin.site.register(OrderPosition, OrderPositionAdmin)
admin.site.register(Coupon, CouponAdmin)






