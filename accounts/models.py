from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateField(auto_now_add=True)
    following = models.ManyToManyField(
        'self', related_name='followers', symmetrical=False
    )
    likes = models.ManyToManyField('posts.Post', related_name='liked_by')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_liked(self, post):
        return self.likes.filter(pk=post.pk).exists()

    def like(self, post):
        if not self.is_liked(post):
            self.likes.add(post)

    def unlike(self, post):
        if self.is_liked(post):
            self.likes.remove(post)
