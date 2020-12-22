from django.test import TestCase, Client
from django.contrib.auth import get_user_model

class MyAuthTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user1 = User.objects.create_user(email = 'user1@gmail.com', password = 'foo1', username = 'dummy1')
        user2 = User.objects.create_user(email = 'user2@gmail.com', password = 'foo2', username = 'dummy2')
        # print("userid" + str(user1.id))
        # print("userid" + str(user2.id))

    def test_user(self):
        self.client = Client()
        user_data = {
            'username': 'foo',
            'password': 'akdsfaklj'
        }
        response1 = self.client.post('/auth/users/', user_data)
        self.assertEqual(response1.status_code, 201)
        response2 = self.client.post('/auth/jwt/create/', user_data)
        self.assertEqual(response2.status_code, 200)

        token = response2.data['access']
        