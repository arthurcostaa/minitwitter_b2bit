from django.test import TestCase

from .models import CustomUser


class CustomUserTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='ana', email='ana@email.com', password='GoodMorning#123'
        )
        self.user2 = CustomUser.objects.create_user(
            username='joao', email='joao@email.com', password='GoodMorning#123'
        )

    def test_follow(self):
        self.user1.follow(self.user2)
        self.assertTrue(self.user1.following.filter(pk=self.user2.pk).exists())

    def test_unfollow(self):
        self.user1.following.add(self.user2)
        self.user1.unfollow(self.user2)
        self.assertFalse(self.user1.following.filter(pk=self.user2.pk).exists())

    def test_user_is_following_another_user(self):
        self.user1.following.add(self.user2)
        self.assertTrue(self.user1.is_following(self.user2))

    def test_user_is_not_following_another_user(self):
        self.assertFalse(self.user1.is_following(self.user2))
