import json

from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.db import connection

from blog.models import BlogPost
from catalog.models import Product, Category, Contact, Version
from users.models import User


class Command(BaseCommand):
    """Класс для кастомной команды заполнения БД"""

    @staticmethod
    def json_read(name_file: str) -> dict:
        """Метод считывает данные из json-файла"""
        with open(name_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def json_read_data(name_app, name_model):
        """Метод читает данные из json-файла по конкретному приложению и модели"""
        data = []

        for item in Command.json_read('catalog_data.json'):
            if item["model"] == f"{name_app}.{name_model}":
                data.append(item)

        return data

    @staticmethod
    def truncate_table_restart_id(name_app, name_model):
        """Метод очищает таблицу и обнуляет id=1"""
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {name_app}_{name_model} RESTART IDENTITY CASCADE')

    @staticmethod
    def select_setval_id(name_app, name_model):
        """Метод устанавливает последний id в таблице"""
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT SETVAL('{name_app}_{name_model}_id_seq', (SELECT MAX(id) FROM {name_app}_{name_model}));")

    def handle(self, *args, **options):
        """Метод для заполнения БД"""

        Command.select_setval_id('users', 'user')

        Product.objects.all().delete()
        Category.objects.all().delete()
        Contact.objects.all().delete()
        Version.objects.all().delete()
        Command.truncate_table_restart_id('catalog', 'product')
        Command.truncate_table_restart_id('catalog', 'category')
        Command.truncate_table_restart_id('catalog', 'contact')
        Command.truncate_table_restart_id('catalog', 'version')

        product_for_create = []
        category_for_create = []
        contact_for_create = []
        version_for_create = []

        for category in Command.json_read_data('catalog', 'category'):
            category_for_create.append(
                Category(id=category["pk"], name=category["fields"]["name"],
                         description=category["fields"]["description"])
            )

        Category.objects.bulk_create(category_for_create)
        Command.select_setval_id('catalog', 'category')

        for product in Command.json_read_data('catalog', 'product'):
            product_for_create.append(
                Product(id=product["pk"], name=product["fields"]["name"], description=product["fields"]["description"],
                        preview=product["fields"]["preview"],
                        category=Category.objects.get(pk=product["fields"]["category"]),
                        price=product["fields"]["price"], created_at=product["fields"]["created_at"],
                        updated_at=product["fields"]["updated_at"],
                        user=User.objects.get(pk=product["fields"]["user"]),
                        is_published=product["fields"]["is_published"]
                        )
            )

        Product.objects.bulk_create(product_for_create)
        Command.select_setval_id('catalog', 'product')

        for contact in Command.json_read_data('catalog', 'contact'):
            contact_for_create.append(
                Contact(id=contact["pk"], name=contact["fields"]["name"], phone=contact["fields"]["phone"],
                        message=contact["fields"]["message"])
            )

        Contact.objects.bulk_create(contact_for_create)
        Command.select_setval_id('catalog', 'contact')

        for version in Command.json_read_data('catalog', 'version'):
            version_for_create.append(
                Version(id=version["pk"], product=Product.objects.get(pk=version["fields"]["product"]),
                        version_number=version["fields"]["version_number"],
                        name_version=version["fields"]["name_version"],
                        is_current_version=version["fields"]["is_current_version"])
            )

        Version.objects.bulk_create(version_for_create)
        Command.select_setval_id('catalog', 'version')

        BlogPost.objects.all().delete()
        Command.truncate_table_restart_id('blog', 'blogpost')

        blogpost_for_create = []
        for blogpost in Command.json_read('blog_data.json'):
            blogpost_for_create.append(
                BlogPost(id=blogpost["pk"], title=blogpost["fields"]["title"], slug=blogpost["fields"]["slug"],
                         content=blogpost["fields"]["content"], preview=blogpost["fields"]["preview"],
                         is_published=blogpost["fields"]["is_published"],
                         views_count=blogpost["fields"]["views_count"],
                         created_at=blogpost["fields"]["created_at"])
            )

        BlogPost.objects.bulk_create(blogpost_for_create)
        Command.select_setval_id('blog', 'blogpost')


