from django.core.cache import cache

from catalog.models import Category
from config import settings


def get_categories_for_cache():
    """Функция получает список категорий продуктов из кэша или из БД и тогда записывает в кэш"""
    if settings.CACHE_ENABLED:
        key = 'categories'
        categories_list = cache.get(key)
        if categories_list is None:
            categories_list = Category.objects.all()
            cache.set(key, categories_list)
    else:
        categories_list = Category.objects.all()

    return categories_list
