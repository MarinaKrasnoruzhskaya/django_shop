import json

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
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
    def json_read_data(name_file, name_app, name_model):
        """Метод читает данные из json-файла по конкретному приложению и модели"""
        data = []

        for item in Command.json_read(name_file):
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
        # таблица contenttypes.contenttype

        ContentType.objects.all().delete()
        Command.truncate_table_restart_id('django', 'content_type')

        contenttype_for_create = []

        for content in Command.json_read_data('contenttypes_data.json', 'contenttypes', 'contenttype'):
            contenttype_for_create.append(
                ContentType(
                    id=content["pk"],
                    app_label=content["fields"]["app_label"],
                    model=content["fields"]["model"])
            )

        ContentType.objects.bulk_create(contenttype_for_create)
        Command.select_setval_id('django', 'content_type')

        # таблица auth.permission

        Permission.objects.all().delete()
        Command.truncate_table_restart_id('auth', 'permission')
        permission_for_create = []

        for perm in Command.json_read_data('auth_data.json', 'auth', 'permission'):
            permission_for_create.append(
                Permission(
                    id=perm["pk"],
                    name=perm["fields"]["name"],
                    content_type=ContentType.objects.get(pk=perm["fields"]["content_type"]),
                    codename=perm["fields"]["codename"],
                )
            )

        Permission.objects.bulk_create(permission_for_create)
        Command.select_setval_id('auth', 'permission')

        # таблица auth.group

        Group.objects.all().delete()
        Command.truncate_table_restart_id('auth', 'group')
        group_for_create = []
        group_permissions = {}

        for group in Command.json_read_data('auth_data.json', 'auth', 'group'):
            permissions = []
            for perm_id in group["fields"]["permissions"]:
                permissions.append(Permission.objects.get(id=perm_id))
            group_permissions[group["pk"]] = permissions

            group_for_create.append(
                Group(
                    id=group["pk"],
                    name=group["fields"]["name"],
                )
            )

        Group.objects.bulk_create(group_for_create)
        Command.select_setval_id('auth', 'group')

        for pk, permissions in group_permissions.items():
            group = Group.objects.get(pk=pk)
            group.permissions.set(permissions)

        # таблица users.user
        User.objects.all().delete()
        Command.truncate_table_restart_id('users', 'user')

        user_for_create = []
        user_groups = {}
        user_permissions = {}
        for user in Command.json_read('users_data.json'):
            permissions = [Permission.objects.get(id=perm_id) for perm_id in user["fields"]["user_permissions"]]
            user_permissions[user["pk"]] = permissions
            groups = [Group.objects.get(pk=group_id) for group_id in user["fields"]["groups"]]
            user_groups[user["pk"]] = groups
            user_for_create.append(
                User(
                    id=user["pk"],
                    password=user["fields"]["password"],
                    last_login=user["fields"]["last_login"],
                    is_superuser=user["fields"]["is_superuser"],
                    is_staff=user["fields"]["is_staff"],
                    is_active=user["fields"]["is_active"],
                    date_joined=user["fields"]["date_joined"],
                    email=user["fields"]["email"],
                    phone_number=user["fields"]["phone_number"],
                    country=user["fields"]["country"],
                    token=user["fields"]["token"],
                    first_name=user["fields"]["first_name"],
                    last_name=user["fields"]["last_name"],
                )
            )

        User.objects.bulk_create(user_for_create)
        Command.select_setval_id('users', 'user')

        for pk, permissions in user_permissions.items():
            user = User.objects.get(pk=pk)
            user.user_permissions.set(permissions)

        for pk, groups in user_groups.items():
            user = User.objects.get(pk=pk)
            user.groups.set(groups)


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

        for category in Command.json_read_data('catalog_data.json', 'catalog', 'category'):
            category_for_create.append(
                Category(id=category["pk"], name=category["fields"]["name"],
                         description=category["fields"]["description"])
            )

        Category.objects.bulk_create(category_for_create)
        Command.select_setval_id('catalog', 'category')

        for product in Command.json_read_data('catalog_data.json', 'catalog', 'product'):
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

        for contact in Command.json_read_data('catalog_data.json', 'catalog', 'contact'):
            contact_for_create.append(
                Contact(id=contact["pk"], name=contact["fields"]["name"], phone=contact["fields"]["phone"],
                        message=contact["fields"]["message"])
            )

        Contact.objects.bulk_create(contact_for_create)
        Command.select_setval_id('catalog', 'contact')

        for version in Command.json_read_data('catalog_data.json', 'catalog', 'version'):
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
                         created_at=blogpost["fields"]["created_at"],
                         author=User.objects.get(pk=blogpost["fields"]["author"]))
            )

        BlogPost.objects.bulk_create(blogpost_for_create)
        Command.select_setval_id('blog', 'blogpost')
