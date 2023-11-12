from django.urls import path
from blog.views import (
	create_blog_view,
    detail_blog_view,
    edit_blog_view,
    add_comment,
    delete_comment,
)

app_name = 'blog'

urlpatterns = [
    path('create', create_blog_view, name="create"),
    path('<slug>', detail_blog_view, name="detail"),
    path('<slug>/edit', edit_blog_view, name="edit"),
    path('<slug>/add-comment', add_comment, name="add-comment"),
    path('<slug>/delete-comment', delete_comment, name="delete-comment"),
]