from django.contrib import admin
from .models import UserProfile, Article, AuthoredThrough

admin.site.register(UserProfile)
admin.site.register(Article)
admin.site.register(AuthoredThrough)



