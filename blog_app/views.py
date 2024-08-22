from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Article, UserProfile
from utilities import RoleRequiredMixin
from django.http import HttpResponseForbidden


class ArticleListView(ListView):
    model = Article
    template_name = 'blog_app/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # Order by published_date in descending order (most recent first)
        # and limit the number of results to 10
        return Article.objects.order_by('-created_at')[:10]


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog_app/article_detail.html'
    context_object_name = 'article'


class ArticleCreateView(RoleRequiredMixin, CreateView):
    required_role = 'Admin'
    model = Article
    fields = ["title", "body"]
    template_name = 'blog_app/article_create.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})


class ArticleUpdateView(RoleRequiredMixin, UpdateView):
    required_role = 'Admin'
    model = Article
    fields = ["title", "body"]

    # to protect data from non-admins on a database_level
    def get_queryset(self):
        if self.request.user.userprofile.role == UserProfile.USER:
            return HttpResponseForbidden("This page is only accessible for admins.")
        return super().get_queryset()
    template_name = 'blog_app/article_update.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})

















