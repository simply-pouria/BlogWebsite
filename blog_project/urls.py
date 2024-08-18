
from django.contrib import admin
from django.urls import path
from blog_app.views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ArticleListView.as_view(), name='home'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article'),
]
