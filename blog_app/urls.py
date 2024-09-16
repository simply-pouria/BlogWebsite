from django.contrib import admin
from django.urls import path, include
from blog_app.views import ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleCreateView, ArticleSignUpView, ArticleDeleteView, DeployWebhookView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/new/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('signup/', ArticleSignUpView.as_view(), name='signup'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('webhook/', DeployWebhookView.as_view(), name='deploy_webhook'),
    
# not used in production, just to serve static files

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


