from django.urls import path
from blog.views import (
	create_blog_view,
    detail_blog_view,
    edit_blog_view,
    ver_blog,
    add_comment,
    like_blog_post,
    like_post,

    
)

from django.conf import settings
from django.conf.urls.static import static
app_name = 'blog'

urlpatterns = [
    path('create/', create_blog_view, name="create"),
    path('<slug>/', detail_blog_view, name="detail"),
    path('<slug>/edit/', edit_blog_view, name="edit"),
    path('<int:blog_id>/', ver_blog, name='ver_blog'),
    path('blog/add_comment/<int:blog_id>/', add_comment, name='add_comment'),
    path('like/', like_blog_post, name='like_blog_post'),
    path('like_post/<int:blog_id>/', like_post, name='like_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)