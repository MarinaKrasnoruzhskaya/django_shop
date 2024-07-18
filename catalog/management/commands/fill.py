import json

from django.core.management import BaseCommand
from django.db import connection

from blog.models import BlogPost
from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read(name_file):
        with open(name_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def json_read_categories():
        categories = []

        for item in Command.json_read('catalog_data.json'):
            if item["model"] == "catalog.category":
                categories.append(item)

        return categories

    @staticmethod
    def json_read_products():
        products = []

        for item in Command.json_read('catalog_data.json'):
            if item["model"] == "catalog.product":
                products.append(item)

        return products

    @staticmethod
    def truncate_table_restart_id(name_app, name_model):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {name_app}_{name_model} RESTART IDENTITY CASCADE')

    @staticmethod
    def select_setval_id(name_app, name_model):
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT SETVAL('{name_app}_{name_model}_id_seq', (SELECT MAX(id) FROM {name_app}_{name_model}));")

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()
        Command.truncate_table_restart_id('catalog', 'product')
        Command.truncate_table_restart_id('catalog','category')

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(
                Category(id=category["pk"], name=category["fields"]["name"],
                         description=category["fields"]["description"])
            )

        Category.objects.bulk_create(category_for_create)
        Command.select_setval_id('catalog','category')

        for product in Command.json_read_products():
            product_for_create.append(
                Product(id=product["pk"], name=product["fields"]["name"], description=product["fields"]["description"],
                        preview=product["fields"]["preview"],
                        category=Category.objects.get(pk=product["fields"]["category"]),
                        price=product["fields"]["price"], created_at=product["fields"]["created_at"],
                        updated_at=product["fields"]["updated_at"])
            )

        Product.objects.bulk_create(product_for_create)
        Command.select_setval_id('catalog','product')

        BlogPost.objects.all().delete()
        Command.truncate_table_restart_id('blog', 'blogpost')

        blogpost_for_create = []
        for blogpost in Command.json_read('blog_data.json'):
            blogpost_for_create.append(
                BlogPost(id=blogpost["pk"], title=blogpost["fields"]["title"], content=blogpost["fields"]["content"],
                         preview=blogpost["fields"]["preview"], is_published=blogpost["fields"]["is_published"],
                         views_count=blogpost["fields"]["views_count"], created_at=blogpost["fields"]["created_at"])
            )

        BlogPost.objects.bulk_create(blogpost_for_create)
        Command.select_setval_id('blog', 'blogpost')
