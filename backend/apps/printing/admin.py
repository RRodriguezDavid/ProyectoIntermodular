from django.contrib import admin
from .models import CustomSTL


@admin.register(CustomSTL)
class CustomSTLAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'nombre_archivo', 'uploaded_at', 'status', 'volume_cm3', 'calculated_price')
    list_filter = ('status', 'uploaded_at')
    search_fields = ('user__username', 'nombre_archivo')
    readonly_fields = ('volume_cm3', 'estimated_weight_gr', 'calculated_price', 'uploaded_at', 'status')
