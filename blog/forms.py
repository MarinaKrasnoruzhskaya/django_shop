from django.forms import ModelForm

from blog.models import BlogPost
from catalog.forms import StyleFormMixin


class BlogPostForm(StyleFormMixin, ModelForm):
    """Форма для редактирования блоговой записи"""
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview']


class BlogPostUpdateForm(StyleFormMixin, ModelForm):
    """Форма для редактирования блоговой записи"""
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview', 'is_published']
