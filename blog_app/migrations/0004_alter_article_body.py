# Generated by Django 4.0.10 on 2024-09-14 08:32

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0003_alter_article_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=markdownx.models.MarkdownxField(null=True),
        ),
    ]