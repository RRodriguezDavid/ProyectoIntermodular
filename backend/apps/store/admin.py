from django.contrib import admin
from .models import Category, Product, STLModel


class STLModelInline(admin.StackedInline):
    model = STLModel
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'tipo')
    list_filter = ('tipo',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'stock', 'activo')
    list_filter = ('category', 'activo')
    list_editable = ('base_price', 'stock', 'activo')
    search_fields = ('name', 'description')
    inlines = [STLModelInline]
