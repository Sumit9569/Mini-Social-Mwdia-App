from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    audio_name = models.CharField(max_length=100, blank=True)
    audio_artist = models.CharField(max_length=100, blank=True)
    audio_link = models.URLField(blank=True)
    tag_people = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=150, blank=True)

    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.author.username} - {self.caption[:30]}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} comment"