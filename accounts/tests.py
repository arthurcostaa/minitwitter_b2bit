from datetime import date

from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework import status
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


class AutheticationViewTest(TestCase):
    def setUp(self):
        password = 'GoodMorning#123'
        self.user = CustomUser.objects.create_user(
            username='ana', email='ana@email.com', password=password
        )
        self.user.clean_password = password

    def test_get_access_and_refresh_token(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={'email': self.user.email, 'password': self.user.clean_password},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

    def test_refresh_token(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={'email': self.user.email, 'password': self.user.clean_password},
            format='json',
        )
        refresh_token = response.json().get('refresh')
        response = self.client.post(
            reverse('token_refresh'),
            data={'refresh': refresh_token},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())

    def test_get_access_token_with_invalid_credentials(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={'email': 'abc@email.com', 'password': 'password'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(
            response.json(),
            {'detail': 'No active account found with the given credentials'},
        )

    def test_refresh_token_with_invalid_refresh_token(self):
        refresh_token = 'InVaLidToKeN'
        response = self.client.post(
            reverse('token_refresh'),
            data={'refresh': refresh_token},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(
            response.json(), {'detail': 'Token is invalid', 'code': 'token_not_valid'}
        )


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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.json(),
            {
                'id': 1,
                'username': 'johndoe',
                'email': 'johndoe@email.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'date_joined': today,
            },
        )
