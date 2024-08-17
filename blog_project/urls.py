
from django.contrib import admin
from django.urls import path
from blog_app.views import ArticleView, ArticlesList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ArticlesList.as_view(), name='home'),
    path('books/', ArticleView.as_view(), name='books'),
]
