from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class UserProfile(models.Model):

    USER = 0
    ADMIN = 1
    ROLE_CHOICES = [
        (USER, 'User'),
        (ADMIN, 'Admin'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # a user is able to have not authored an article have
    authored = models.ManyToManyField('Article', through='AuthoredThrough', blank=True)
    role = models.IntegerField(default=USER, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class Article(models.Model):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(4, "Title must be greater than 4 characters")],
    )
    body = MarkdownxField(null=True)
    authors = models.ManyToManyField('UserProfile', through='AuthoredThrough', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Convert the body to HTML when rendering
    def formatted_markdown(self):
        return markdownify(self.body)
    def __str__(self):
        return self.title


# Through Table to handle the Many-To-Many relationship
class AuthoredThrough(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)



