from django.test import TestCase

from accounts.models import CustomUser
from posts.models import Post


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='ana', email='ana@email.com', password='GoodMorning#123'
        )
        self.user2 = CustomUser.objects.create_user(
            username='joao', email='joao@email.com', password='GoodMorning#123'
        )
        self.post = Post.objects.create(author=self.user2, content='xyz')

    def test_follow(self):
        self.user1.follow(self.user2)
        self.assertTrue(self.user1.following.filter(pk=self.user2.pk).exists())

    def test_unfollow(self):
        self.user1.following.add(self.user2)
        self.user1.unfollow(self.user2)
        self.assertFalse(self.user1.following.filter(pk=self.user2.pk).exists())

    def test_user_is_following_another_user(self):
        self.user1.follow(self.user2)
        self.assertTrue(self.user1.is_following(self.user2))

    def test_user_is_not_following_another_user(self):
        self.assertFalse(self.user1.is_following(self.user2))

    def test_like(self):
        self.user1.like(self.post)
        self.assertTrue(self.user1.likes.filter(pk=self.post.pk).exists())

    def test_unlike(self):
        self.user1.likes.add(self.post)
        self.user1.unlike(self.post)
        self.assertFalse(self.user1.likes.filter(pk=self.post.pk).exists())

    def test_user_liked_post(self):
        self.user1.like(self.post)
        self.assertTrue(self.user1.is_liked(self.post))

    def test_user_dont_like_post(self):
        self.assertFalse(self.user1.is_liked(self.post))
