from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'blog_app/article_detail.html'  # unfinished
    context_object_name = 'articles'

    def get_queryset(self):
        # Order by published_date in descending order (most recent first)
        # and limit the number of results to 10
        return Article.objects.order_by('-created_at')[:10]


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog_app/article_detail.html'  # unfinished
    context_object_name = 'article'

















