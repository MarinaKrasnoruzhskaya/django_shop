import json

from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read():
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def json_read_categories():
        categories = []

        for item in Command.json_read():
            if item["model"] == "catalog.category":
                categories.append(item)

        return categories

    @staticmethod
    def json_read_products():
        products = []

        for item in Command.json_read():
            if item["model"] == "catalog.product":
                products.append(item)

        return products

    @staticmethod
    def truncate_table_restart_id(name_model):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE catalog_{name_model} RESTART IDENTITY CASCADE')

    @staticmethod
    def select_setval_id(name_model):
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT SETVAL('catalog_{name_model}_id_seq', (SELECT MAX(id) FROM catalog_{name_model}));")

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()
        Command.truncate_table_restart_id('product')
        Command.truncate_table_restart_id('category')

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(
                Category(id=category["pk"], name=category["fields"]["name"],
                         description=category["fields"]["description"])
            )

        Category.objects.bulk_create(category_for_create)
        Command.select_setval_id('category')

        for product in Command.json_read_products():
            product_for_create.append(
                Product(id=product["pk"], name=product["fields"]["name"], description=product["fields"]["description"],
                        preview=product["fields"]["preview"],
                        category=Category.objects.get(pk=product["fields"]["category"]),
                        price=product["fields"]["price"], created_at=product["fields"]["created_at"],
                        updated_at=product["fields"]["updated_at"])
            )

        Product.objects.bulk_create(product_for_create)
        Command.select_setval_id('product')
