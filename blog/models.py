from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import bleach


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete= models.CASCADE)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Generate slug from title if not set
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            n = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        # Sanitize rich text content to prevent XSS while allowing basic formatting
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 'ul', 'ol', 'li', 'a', 'blockquote', 'code', 'pre', 'h1', 'h2', 'h3',
            'h4', 'h5', 'h6', 'span'
        ]
        allowed_attrs = {
            'a': ['href', 'title', 'target', 'rel'],
            'span': ['style'],
        }
        self.content = bleach.clean(self.content or '', tags=allowed_tags, attributes=allowed_attrs, strip=True)
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Sanitize rich text content to prevent XSS while allowing basic formatting
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 'ul', 'ol', 'li', 'a', 'blockquote', 'code', 'pre', 'h1', 'h2', 'h3',
            'h4', 'h5', 'h6', 'span'
        ]
        allowed_attrs = {
            'a': ['href', 'title', 'target', 'rel'],
            'span': ['style'],
        }
        self.content = bleach.clean(self.content or '', tags=allowed_tags, attributes=allowed_attrs, strip=True)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

    def save(self, *args, **kwargs):
        # Sanitize comment content as plain text with basic formatting
        allowed_tags = ['strong', 'em', 'u', 'code', 'br']
        self.content = bleach.clean(self.content or '', tags=allowed_tags, strip=True)
        super().save(*args, **kwargs)