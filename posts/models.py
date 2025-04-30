from django.db import models

from accounts.models import CustomUser


class Post(models.Model):
    author = models.ForeignKey(
        CustomUser, related_name='posts', on_delete=models.CASCADE
    )
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.content[:20]}'
