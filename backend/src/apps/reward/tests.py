from django.test import TestCase, Client

class RewardTests(TestCase):
    token = ''
    user_id = -1

    def setUp(self):
        self.client = Client()
        user_data = {
            'username': 'foo',
            'password': 'akdsfaklj'
        }
        response1 = self.client.post('/auth/users/', user_data)
        self.assertEqual(response1.status_code, 201)
        response2 = self.client.post('/auth/jwt/create/', user_data)
        self.assertEqual(response2.status_code, 200)

        self.token = response2.data['access']

        response3 = self.client.post('/auth/jwt/verify/', {'token' : self.token})
        self.assertEqual(response3.status_code, 200)

        # get user's id
        response4 = self.client.get('/auth/users/me/', HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response4.status_code, 200)
        self.user_id = response4.data['id']
        
        #create game
        response5 = self.client.post('/game/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response5.status_code, 200)
    
    def test_create(self):
        response1 = self.client.post('/reward/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response1.status_code, 200)