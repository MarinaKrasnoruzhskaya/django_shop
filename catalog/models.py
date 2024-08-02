from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    """Класс для категорий продуктов"""
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории',
        help_text='Введите название категории',
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        **NULLABLE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    """Класс для продуктов"""
    name = models.CharField(
        max_length=100,
        verbose_name='Название продукта',
        help_text='Введите название продукта',
    )
    description = models.TextField(
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
        **NULLABLE,
    )
    preview = models.ImageField(
        upload_to='products',
        verbose_name="Изображение",
        help_text="Загрузите изображение продукта",
        **NULLABLE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию продукта",
        related_name='products',
        **NULLABLE,
    )
    price = models.IntegerField(
        verbose_name="Цена за покупку",
        help_text="Введите цену за покупку",
    )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата последнего изменения", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ('name',)


class Version(models.Model):
    """Класс для версии продукта"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        help_text='Выберите продукт',
        related_name='versions'
    )
    version_number = models.PositiveIntegerField(
        verbose_name='Номер версии',
        help_text='Введите номер версии'
    )
    name_version = models.CharField(
        max_length=100,
        verbose_name='Название версии',
        help_text='Введите название версии'
    )
    is_current_version = models.BooleanField(
        default=False,
        verbose_name='Это текущая версия',
        help_text='Установите текущую версию'
    )

    def __str__(self):
        return f'{self.product.name} - {self.version_number}'

    class Meta:
        verbose_name = 'Версия продукта'
        verbose_name_plural = 'Версии продукта'
        ordering = ('-version_number',)

class Contact(models.Model):
    """Класс для контактов"""
    name = models.CharField(max_length=100, verbose_name='Имя', help_text='Введите имя',)
    phone = models.CharField(max_length=15, verbose_name='Телефон', help_text='Введите телефон',)
    message = models.TextField(verbose_name='Сообщение', help_text='Введите сообщение',)

    def __str__(self):
        return f'{self.name} - {self.phone}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ('-id',)
