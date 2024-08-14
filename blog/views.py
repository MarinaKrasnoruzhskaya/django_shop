import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from dotenv import load_dotenv
from pytils.translit import slugify

from blog.models import BlogPost

load_dotenv()


class BlogPostListView(ListView):
    """Контроллер для вывода списка постов"""
    model = BlogPost

    def get_queryset(self, *args, **kwargs):
        """Метод возвращает для контент-менеджера все посты, для остальных пользователей только опубликованные"""
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        user_group = Group.objects.filter(user=user).first()
        group = Group.objects.get(name='content-manager')
        if user_group and user_group.pk == group.pk or user.is_superuser:
            return queryset
        else:
            queryset = queryset.filter(is_published=True)
            return queryset


class BlogPostDetailView(DetailView):
    """Контроллер для просмотра одного поста"""
    model = BlogPost

    def get_object(self, queryset=None):
        """Метод ведет подсчет количества просмотров и при достижении 100 просмотров отправляет сообщение"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save(update_fields=['views_count'])
        if self.object.views_count == 100:
            send_mail(
                subject="Новое достижение",
                message=f"Поздравляем! Вашу запись {self.object.title} просмотрели {self.object.views_count} раз. "
                        f"С уважением Ваш Bow-shop!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[os.getenv("EMAIL_USER"),],
            )
        return self.object


class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер для создания поста"""
    model = BlogPost
    fields = ('title', 'content', 'preview', 'is_published')
    permission_required = 'blog.add_blogpost'
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()

        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для изменения поста"""
    model = BlogPost
    fields = ('title', 'content', 'preview', 'is_published')
    permission_required = 'blog.change_blogpost'

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogPostDeleteView(DeleteView):
    """Контроллер для удаления поста"""
    model = BlogPost
    success_url = reverse_lazy("blog:list")
    permission_required = 'blog.delete_blogpost'
