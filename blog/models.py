from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class BlogPost(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок', help_text='Введите заголовок', )
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE, )
    content = models.TextField(verbose_name='Содержимое', help_text='Введите содержимое', **NULLABLE, )
    preview = models.ImageField(upload_to='blog/', verbose_name='Превью', help_text="Загрузите превью",
                                **NULLABLE, )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True, )
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано', help_text='Опубликовать блог?')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры', help_text='Количество просмотров блога',
                                      editable=False)
    author = models.ForeignKey(User, verbose_name='Автор', help_text='Укажите автора', **NULLABLE, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блоговая запись>"
        verbose_name_plural = "Блоговые записи"
        ordering = ('title',)
