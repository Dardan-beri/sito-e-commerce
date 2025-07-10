from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):  # oppure StackedInline
    model = OrderItem
    extra = 0  # Nessuna riga vuota extra
    readonly_fields = ('product', 'quantity', 'price')  # opzionale

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total', 'is_cancelled')
    list_filter = ('is_cancelled', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
