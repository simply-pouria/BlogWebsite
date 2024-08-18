
from django.contrib import admin
from django.urls import path
from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('admin/<int:pk>', admin.site.urls),
    path('', ArticleListView.as_view(), name='home'),
    path('article/', ArticleDetailView.as_view(), name='article'),
]
