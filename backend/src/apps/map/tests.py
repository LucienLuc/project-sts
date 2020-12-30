from django.test import TestCase, Client

class MapTests(TestCase):
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

    def test_generate_map(self):    
        response1 = self.client.post('/map/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response1.status_code, 201)

    def test_move(self):
        response1 = self.client.post('/map/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response1.status_code, 201)

        response_state = self.client.get('/map/' + str(self.user_id) + '/get_state/', HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        # print(response_state.data)
        self.assertEqual(response_state.status_code, 200)

        #invalid move
        response2 = self.client.post('/map/' + str(self.user_id) + '/move/', {'next_position': 6}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response2.status_code, 409)

        response_state = self.client.get('/map/' + str(self.user_id) + '/get_state/', HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response_state.data['position'], -1)
        self.assertEqual(response_state.status_code, 200)

        response3 = self.client.post('/map/' + str(self.user_id) + '/move/', {'next_position': 0}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response3.status_code, 200)
        
        response_state = self.client.get('/map/' + str(self.user_id) + '/get_state/', HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response_state.data['position'], 0)
        self.assertEqual(response_state.status_code, 200)
        valid_moves = response_state.data['game_map']['0']
        next_move = valid_moves[0]

        response4 = self.client.post('/map/' + str(self.user_id) + '/move/', {'next_position': next_move}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response4.status_code, 200)

        response_state = self.client.get('/map/' + str(self.user_id) + '/get_state/', HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response_state.data['position'], next_move)
        self.assertEqual(response_state.status_code, 200)