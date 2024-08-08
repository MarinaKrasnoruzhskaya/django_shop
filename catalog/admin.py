from django.contrib import admin
from catalog.models import Product, Category, Contact, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий прод"""
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для продуктов"""
    list_display = ('id', 'name', 'price', 'category', 'user')
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    """Админка для версий продуктов"""
    list_display = ('id', 'product', 'version_number', 'name_version', 'is_current_version')
    list_filter = ('product', 'is_current_version')
    search_fields = ('product__name', 'name_version')


@admin.register(Contact)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'message')
