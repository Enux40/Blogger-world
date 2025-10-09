
from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from .models import Post, Comment


@override_settings(ROOT_URLCONF='blog_proj.urls', STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PostTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='alice', password='password123')

	def test_create_post_requires_login(self):
		url = reverse('post-create')
		self.assertEqual(url, '/post/new/')
		# GET should redirect to login
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)
		self.assertIn('/login/', resp.headers.get('Location', ''))
		# POST should also redirect to login
		resp2 = self.client.post(url, {'title': 'Test', 'content': 'Test'})
		self.assertEqual(resp2.status_code, 302)
		self.assertIn('/login/', resp2.headers.get('Location', ''))

	def test_create_post_success(self):
		self.client.login(username='alice', password='password123')
		url = reverse('post-create')
		self.assertEqual(url, '/post/new/')
		# GET the form
		resp_form = self.client.get(url)
		self.assertEqual(resp_form.status_code, 200)
		# POST to create
		resp = self.client.post(url, {
			'title': 'Hello',
			'content': '<p>World</p>'
		})
		self.assertIn(resp.status_code, [302, 200])
		post = Post.objects.get(title='Hello')
		self.assertEqual(post.author, self.user)
		self.assertIn('World', post.content)
		self.assertTrue(post.slug)
		detail_url = reverse('post-detail', kwargs={'slug': post.slug})
		resp2 = self.client.get(detail_url)
		self.assertEqual(resp2.status_code, 200)


@override_settings(ROOT_URLCONF='blog_proj.urls', STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class CommentTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='bob', password='password123')
		self.post = Post.objects.create(title='Post', content='content', author=self.user)
		self.post.save()
		# Ensure slug is set
		if not self.post.slug:
			self.post.slug = slugify(self.post.title)
			self.post.save()

	def test_add_comment_requires_login(self):
		url = reverse('post-add-comment', kwargs={'slug': self.post.slug})
		resp = self.client.post(url, {'content': 'Hi'})
		self.assertIn(resp.status_code, [302, 403])

	def test_add_comment_success(self):
		self.client.login(username='bob', password='password123')
		url = reverse('post-add-comment', kwargs={'slug': self.post.slug})
		resp = self.client.post(url, {'content': 'Nice post'})
		self.assertIn(resp.status_code, [302, 200])
		self.assertEqual(Comment.objects.filter(post=self.post).count(), 1)
