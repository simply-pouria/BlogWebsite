
from django.contrib import admin
from django.urls import path, include
from blog_app.views import ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleCreateView

app_name = 'blog_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ArticleListView.as_view(), name='Home'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='ArticleView'),
    path('article/new/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update')
]
