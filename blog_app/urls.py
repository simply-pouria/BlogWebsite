
from django.contrib import admin
from django.urls import path, include
from blog_app.views import ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleCreateView, SignUpView

app_name = 'blog_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/new/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('signup/', SignUpView.as_view(), name='signup')
]
