from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post
from django.utils import timezone


class PostModelTest(TestCase):
    """Test the Post model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content for the post',
            author=self.user
        )
    
    def test_post_creation(self):
        """Test that a post can be created"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'Test content for the post')
        self.assertEqual(self.post.author, self.user)
        self.assertIsNotNone(self.post.date_posted)
    
    def test_post_str_method(self):
        """Test the string representation of a post"""
        self.assertEqual(str(self.post), 'Test Post')
    
    def test_post_get_absolute_url(self):
        """Test the get_absolute_url method"""
        url = self.post.get_absolute_url()
        self.assertEqual(url, f'/post/{self.post.pk}/')


class PostListViewTest(TestCase):
    """Test the PostListView"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Create multiple posts
        for i in range(10):
            Post.objects.create(
                title=f'Test Post {i}',
                content=f'Test content {i}',
                author=self.user
            )
    
    def test_post_list_view_status_code(self):
        """Test that the home page returns a 200 status code"""
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
    
    def test_post_list_view_template(self):
        """Test that the correct template is used"""
        response = self.client.get(reverse('blog-home'))
        self.assertTemplateUsed(response, 'blog/home.html')
    
    def test_post_list_view_pagination(self):
        """Test that pagination works correctly"""
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        # Should have 5 posts per page
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['posts']), 5)
    
    def test_post_list_ordering(self):
        """Test that posts are ordered by date_posted descending"""
        response = self.client.get(reverse('blog-home'))
        posts = response.context['posts']
        # First post should be the most recent
        for i in range(len(posts) - 1):
            self.assertGreaterEqual(posts[i].date_posted, posts[i+1].date_posted)


class PostDetailViewTest(TestCase):
    """Test the PostDetailView"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
    
    def test_post_detail_view_status_code(self):
        """Test that the post detail page returns a 200 status code"""
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_post_detail_view_template(self):
        """Test that the correct template is used"""
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(response, 'blog/post_detail.html')
    
    def test_post_detail_view_context(self):
        """Test that the correct post is in the context"""
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.context['post'].title, 'Test Post')


class PostCreateViewTest(TestCase):
    """Test the PostCreateView"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_post_create_view_redirect_if_not_logged_in(self):
        """Test that non-logged in users are redirected to login"""
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_post_create_view_logged_in(self):
        """Test that logged in users can access the create post page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)
    
    def test_post_create_view_creates_post(self):
        """Test that a post can be created"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('post-create'), {
            'title': 'New Test Post',
            'content': 'New test content'
        })
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, 'New Test Post')
        self.assertEqual(Post.objects.first().author, self.user)


class PostUpdateViewTest(TestCase):
    """Test the PostUpdateView"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
    
    def test_post_update_view_redirect_if_not_logged_in(self):
        """Test that non-logged in users are redirected to login"""
        response = self.client.get(reverse('post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_post_update_view_logged_in_as_author(self):
        """Test that the author can access the update page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_post_update_view_forbidden_for_non_author(self):
        """Test that non-authors cannot update the post"""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 403)
    
    def test_post_update_view_updates_post(self):
        """Test that a post can be updated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('post-update', kwargs={'pk': self.post.pk}), {
            'title': 'Updated Title',
            'content': 'Updated content'
        })
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.content, 'Updated content')


class PostDeleteViewTest(TestCase):
    """Test the PostDeleteView"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
    
    def test_post_delete_view_redirect_if_not_logged_in(self):
        """Test that non-logged in users are redirected to login"""
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_post_delete_view_logged_in_as_author(self):
        """Test that the author can access the delete page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_post_delete_view_forbidden_for_non_author(self):
        """Test that non-authors cannot delete the post"""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 403)
    
    def test_post_delete_view_deletes_post(self):
        """Test that a post can be deleted"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(Post.objects.count(), 0)


class UserPostListViewTest(TestCase):
    """Test the UserPostListView"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        # Create posts for testuser
        for i in range(5):
            Post.objects.create(
                title=f'Test Post {i}',
                content=f'Test content {i}',
                author=self.user
            )
        # Create posts for otheruser
        for i in range(3):
            Post.objects.create(
                title=f'Other Post {i}',
                content=f'Other content {i}',
                author=self.other_user
            )
    
    def test_user_post_list_view_status_code(self):
        """Test that the user posts page returns a 200 status code"""
        response = self.client.get(reverse('user-posts', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
    
    def test_user_post_list_view_shows_only_user_posts(self):
        """Test that only the specified user's posts are shown"""
        response = self.client.get(reverse('user-posts', kwargs={'username': 'testuser'}))
        posts = response.context['posts']
        self.assertEqual(len(posts), 5)
        for post in posts:
            self.assertEqual(post.author.username, 'testuser')
    
    def test_user_post_list_view_404_for_nonexistent_user(self):
        """Test that a 404 is returned for a nonexistent user"""
        response = self.client.get(reverse('user-posts', kwargs={'username': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)


class AboutViewTest(TestCase):
    """Test the about view"""
    
    def setUp(self):
        self.client = Client()
    
    def test_about_view_status_code(self):
        """Test that the about page returns a 200 status code"""
        response = self.client.get(reverse('blog-about'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_view_template(self):
        """Test that the correct template is used"""
        response = self.client.get(reverse('blog-about'))
        self.assertTemplateUsed(response, 'blog/about.html')
