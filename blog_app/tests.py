from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, AuthoredThrough, UserProfile


class HomepageContentTests(TestCase):
    def test_anonymous_homepage_has_academic_sections_and_auth_links(self):
        response = self.client.get(reverse('blog_app:article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/article_list.html')
        self.assertContains(response, 'Pouria Moradpour')
        self.assertContains(response, 'Computer Science Undergraduate')
        self.assertContains(response, 'id="research-title"')
        self.assertContains(response, 'Research')
        self.assertContains(response, 'Interests')
        self.assertContains(response, 'id="writing-title"')
        self.assertContains(response, 'Notes')
        self.assertContains(response, 'Writing')
        self.assertContains(response, 'id="about-title"')
        self.assertContains(response, 'About')
        self.assertContains(response, 'id="contact-title"')
        self.assertContains(response, 'Touch')
        self.assertContains(response, reverse('login'))
        self.assertContains(response, reverse('blog_app:signup'))

    def test_homepage_empty_state_is_preserved(self):
        response = self.client.get(reverse('blog_app:article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['articles']), [])
        self.assertContains(response, 'No articles available.')


class HomepageArticleTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='homepage-author',
            password='test-password',
        )
        now = timezone.now()
        self.articles = []

        for index in range(4):
            article = Article.objects.create(
                title=f'Article {index + 1}',
                body=f'Body for article {index + 1}',
            )
            Article.objects.filter(pk=article.pk).update(
                created_at=now - timedelta(days=index)
            )
            article.refresh_from_db()
            AuthoredThrough.objects.create(
                author=self.author.userprofile,
                article=article,
            )
            self.articles.append(article)

    def test_homepage_contains_only_three_newest_articles_in_order(self):
        response = self.client.get(reverse('blog_app:article_list'))

        homepage_articles = list(response.context['articles'])
        self.assertEqual(homepage_articles, self.articles[:3])
        self.assertEqual(len(homepage_articles), 3)

        for article in self.articles[:3]:
            self.assertContains(response, article.title)
            self.assertContains(
                response,
                reverse('blog_app:article_detail', args=[article.pk]),
            )

        self.assertNotContains(response, self.articles[3].title)


class HomepageAuthenticationTests(TestCase):
    def setUp(self):
        self.normal_user = User.objects.create_user(
            username='normal-user',
            password='test-password',
        )
        self.admin_user = User.objects.create_user(
            username='admin-user',
            password='test-password',
        )
        self.admin_user.userprofile.role = UserProfile.ADMIN
        self.admin_user.userprofile.save()

    def test_authenticated_homepage_keeps_username_and_logout(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('blog_app:article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Logged in as')
        self.assertContains(response, self.normal_user.username)
        self.assertContains(response, reverse('logout'))

    def test_admin_role_sees_article_creation_link(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('blog_app:article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('blog_app:article_create'))
        self.assertContains(response, 'Add an Article')

    def test_normal_user_does_not_gain_admin_controls(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('blog_app:article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, reverse('blog_app:article_create'))