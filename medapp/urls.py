from django.urls import path,include
from .views import *

urlpatterns = [
    path('',blogs,name='blogs'),
    path('bloq/<slug>',blog,name='blog'),
    path('comment',comment,name='comment'),
    path('blog_create',blog_create,name='blog_create'),
    path('delete_blog/<int:id>/', delete_blog, name='delete_blog'),
]