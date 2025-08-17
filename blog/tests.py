from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_blog_home_page_status_code(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_page_status_code(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_create_view(self):
        response = self.client.post(reverse('post-create'), {'title': 'New Post', 'content': 'New Content'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'New Post')

    def test_post_update_view(self):
        response = self.client.post(reverse('post-update', kwargs={'pk': self.post.pk}), {'title': 'Updated Post', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
