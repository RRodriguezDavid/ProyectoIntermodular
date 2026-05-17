from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'custom_stl', 'quantity', 'price_at_purchase', 'subtotal')

    def subtotal(self, obj):
        return f"{obj.subtotal} euros"
    subtotal.short_description = "Subtotal"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price', 'ciudad_envio')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('user__username', 'user__email', 'id')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').order_by('-created_at')
