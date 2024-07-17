from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogPostListView.as_view(), name='list'),
    path('view/<int:pk>/', BlogPostDetailView.as_view(), name='view'),
    path('create/', BlogPostCreateView.as_view(), name='create'),
    path('update/<int:pk>/', BlogPostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BlogPostDeleteView.as_view(), name='delete'),
]
