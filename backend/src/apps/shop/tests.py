from django.test import TestCase, Client

class ShopTests(TestCase):
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
        #create shop
        response1 = self.client.post('/shop/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response1.status_code, 201)

        response_state = self.client.get('/shop/' + str(self.user_id) + '/get_state/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response_state.status_code, 200)

    def test_purchase(self):
        #create shop
        response1 = self.client.post('/shop/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response1.status_code, 201)

        response_state = self.client.get('/shop/' + str(self.user_id) + '/get_state/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response_state.status_code, 200)

        response2 = self.client.post('/shop/' + str(self.user_id) + '/purchase/', {'id': self.user_id, 'selection': 'relic1'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response2.status_code, 200)

        response_state = self.client.get('/shop/' + str(self.user_id) + '/get_state/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response_state.status_code, 200)
        # print(response_state.data)