from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog_app.urls')),  # Include blog_app's URLs with its namespace
    path('accounts/', include('django.contrib.auth.urls')),
    path('markdownx/', include('markdownx.urls')),

]