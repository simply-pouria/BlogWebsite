from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Article, UserProfile, AuthoredThrough
from .utilities import RoleRequiredMixin
from django.http import HttpResponseForbidden


class ArticleListView(ListView):
    model = Article
    template_name = 'blog_app/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # Order by published_date in descending order (most recent first)
        # and limit the number of results to 10
        return Article.objects.order_by('-created_at')[:10]

    # adding the additional context from Userprofile model that is needed to show/hide the "create" button
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            context['user_role'] = user_profile.role
        else:
            context['user_role'] = None

        context['ADMIN_ROLE'] = UserProfile.ADMIN



class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog_app/article_detail.html'
    context_object_name = 'article'

    # adding the additional context from Userprofile model that is needed to show/hide the "update" button
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            context['user_role'] = user_profile.role
        else:
            context['user_role'] = None

        context['ADMIN_ROLE'] = UserProfile.ADMIN



class ArticleCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    required_role = UserProfile.ADMIN
    model = Article
    fields = ["title", "body"]
    template_name = 'blog_app/article_create.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Save the article first to get the instance
        response = super().form_valid(form)
        # Add the current user as an author of the article
        authored = AuthoredThrough(author=self.request.user.userprofile, article=self.object)
        authored.save()

        return response  # to ensure get_success_url works


class ArticleUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    required_role = UserProfile.ADMIN
    model = Article
    fields = ["title", "body"]

    # to protect data from non-admins on a database_level
    def get_queryset(self):
        if self.request.user.userprofile.role == UserProfile.USER:
            return HttpResponseForbidden("This page is only accessible for admins.")
        return super().get_queryset()
    template_name = 'blog_app/article_update.html'

    def get_success_url(self):
        authored = AuthoredThrough(author=self.request.user, article=self.object)
        authored.save()
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Save the article first to get the instance
        response = super().form_valid(form)
        # Add the current user as an author of the article
        authored = AuthoredThrough(author=self.request.user.userprofile, article=self.object)
        authored.save()

        return response  # to ensure get_success_url works


















