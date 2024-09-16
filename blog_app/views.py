import os
import logging
import subprocess

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, UserProfile, AuthoredThrough
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator

from .utilities import RoleRequiredMixin

class ArticleListView(ListView):
    model = Article
    template_name = 'blog_app/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # Order by published_date in descending order (most recent first)
        # and limit the number of results to 3
        return Article.objects.order_by('-created_at')[:3]

    # adding the additional context from Userprofile model that is needed to show/hide the "create" button
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            context['user_role'] = user_profile.role
        else:
            context['user_role'] = None

        context['ADMIN_ROLE'] = UserProfile.ADMIN

        return context



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

        return context


class ArticleCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    required_role = UserProfile.ADMIN
    model = Article
    fields = ["title", "body"]
    template_name = 'blog_app/article_create.html'

    def get_success_url(self):
        return reverse_lazy('blog_app:article_detail', kwargs={'pk': self.object.pk})

    # saving user to the database automatically
    def form_valid(self, form):
        # Save the article first to get the instance
        response = super().form_valid(form)

        # Add the current user as an author of the article
        authored = AuthoredThrough(author=self.request.user.userprofile, article=self.object)
        authored.save()

        return response  # to ensure get_success_url() works as intended


class ArticleUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    required_role = UserProfile.ADMIN
    model = Article
    fields = ["title", "body"]
    template_name = 'blog_app/article_update.html'

    # to protect data from non-admins on a database_level
    def get_queryset(self):
        if self.request.user.userprofile.role == UserProfile.USER:
            return HttpResponseForbidden("This page is only accessible for admins.")
        return super().get_queryset()

    def get_success_url(self):
        return reverse_lazy('blog_app:article_detail', kwargs={'pk': self.object.pk})

    # saving user to the database automatically, if not duplicate
    def form_valid(self, form):
        # Save the article first to get the instance
        response = super().form_valid(form)
        # Check if the author-article relationship already exists, if it doesn't add it
        authored_exists = AuthoredThrough.objects.filter(
            author=self.request.user.userprofile,
            article=self.object
        ).exists()

        if not authored_exists:
            authored = AuthoredThrough(author=self.request.user.userprofile, article=self.object)
            authored.save()

        return response  # to ensure get_success_url works as intended


class ArticleSignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')  # Redirect to login page after successful sign-up


class ArticleDeleteView(RoleRequiredMixin, DeleteView):
    required_role = UserProfile.ADMIN
    model = Article
    template_name = 'blog_app/article_confirm_delete.html'
    success_url = reverse_lazy('blog_app:article_list')


logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class DeployWebhookView(View):
    def post(self, request, *args, **kwargs):
        script_path = '/home/YOUR_PYTHONANYWHERE_USERNAME/YOUR_REPOSITORY/deploy.sh'

        if os.path.exists(script_path):
            logger.info(f'Script exists at {script_path}. Running the script.')
            try:
                subprocess.run([script_path], check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f'Error running the script: {e}')
                return HttpResponse(f'Script execution failed: {e}', status=500)
        else:
            logger.error(f'Script not found at {script_path}')
            return HttpResponse(f'Script not found at {script_path}', status=404)

        return HttpResponse('Deployment triggered')

    def get(self, request, *args, **kwargs):
        return HttpResponse('Not allowed', status=405)


















