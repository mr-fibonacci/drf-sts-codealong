from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='a', password='pass')

    def test_can_list_posts(self):
        a = User.objects.get(username='a')
        Post.objects.create(owner=a, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data, len(response.data))

    def test_anon_cant_create_post(self):
        response = self.client.post('/posts/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_create_post(self):
        self.client.login(username='a', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        a = User.objects.create_user(username='a', password='pass')
        b = User.objects.create_user(username='b', password='pass')
        Post.objects.create(owner=a, title='a title', content='a content')
        Post.objects.create(owner=b, title='b title', content='b content')

    def test_anon_can_retrieve_valid_post(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anon_cant_retrieve_invalid_post(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_update_somebodys_post(self):
        self.client.login(username='a', password='pass')
        response = self.client.put('/posts/2/', {'title': 'yay'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
