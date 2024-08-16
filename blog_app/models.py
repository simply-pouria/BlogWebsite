from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Role(models.Model):
    role_name = models.CharField(max_length=100, unique=True)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    authors = models.ManyToManyField('Article', through='AuthoredThrough')
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Article(models.Model):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(4, "Title must be greater than 4 characters")],
    )
    body = models.TextField(null=True)
    authors = models.ManyToManyField('UserProfile', through='AuthoredThrough')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Through Table to handle the Many-To-Many relationship
class AuthoredThrough(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


# Signal to create or update UserProfile whenever a User is created or updated
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
