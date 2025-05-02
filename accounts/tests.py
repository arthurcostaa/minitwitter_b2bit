from datetime import date

from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient

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


class CustomUserViewSetTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = APIClient()

    def test_create_new_user(self):
        today = date.today().isoformat()
        response = self.client.post(
            reverse('user-list'),
            data={
                'username': 'johndoe',
                'email': 'johndoe@email.com',
                'password': 'StrongP4ssw0rd#314',
                'first_name': 'John',
                'last_name': 'Doe',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.json(),
            {
                'id': 1,
                'username': 'johndoe',
                'email': 'johndoe@email.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'date_joined': today,
            }
        )
