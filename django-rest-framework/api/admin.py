from django.contrib import admin

from .models import Order, OrderItem, Product, User

admin.site.register(User)
admin.site.register(Product)


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]


admin.site.register(Order, OrderAdmin)
