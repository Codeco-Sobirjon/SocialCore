from django.urls import path

from apps.blog.views import (
    BlogListView, BlogDetailView,
    DirectoryListView, DirectoryDetailView
)

urlpatterns = [
    path('list/', BlogListView.as_view(), name='blog-list'),
    path('list/<int:id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('directories/', DirectoryListView.as_view(), name='directory-list'),
    path('directories/<int:id>/', DirectoryDetailView.as_view(), name='directory-detail'),
]
