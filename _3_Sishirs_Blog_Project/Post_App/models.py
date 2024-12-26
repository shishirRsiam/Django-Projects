import os, uuid
from django.db import models
from django.contrib.auth.models import User
from Categories_App.models import Categories
from django.utils.text import slugify
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=1)
    content_file = models.FileField(upload_to='post_content/', null=True, blank=True)
    categories = models.ManyToManyField(Categories)
    views = models.IntegerField(default=0)
    like = models.IntegerField(default=0)

    slug_url = models.SlugField(unique=True, max_length=250, null=1)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug_url:
            self.slug_url = slugify(self.title)

            if not self.slug_url or Post.objects.filter(slug_url=self.slug_url).exists():
                self.slug_url += str(uuid.uuid4())
        super(Post, self).save(*args, **kwargs)


    def get_content_file_path(self):
        """Generate a file path for the content file based on the post ID or slug."""
        return os.path.join(settings.MEDIA_ROOT, 'posts', f"{self.slug_url}.txt")

    def get_content(self):
        """Retrieve the content from the text file."""
        file_path = self.get_content_file_path()
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content =  file.read()
                return content
        return ""

    def set_content(self, content):
        """Save the content to a text file."""
        file_path = self.get_content_file_path()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(content)
