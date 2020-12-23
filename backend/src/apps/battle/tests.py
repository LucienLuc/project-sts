from django.test import TestCase, Client
from src.enemy.enemy import Enemy as ClassEnemy
from src.enemy.enemy import EnemyEncoder
from src.enemy.enemies import *

import json
class BattleTests(TestCase):

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
        response1 = self.client.post('/battle/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response1.status_code, 201)

    def test_play_card(self):
        # Add strike card to deck
        response1 = self.client.post('/game/' + str(self.user_id) + '/add_card_to_deck/', {'card_name': 'Strike'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response1.status_code, 200)

        response2 = self.client.post('/game/' + str(self.user_id) + '/add_card_to_deck/', {'card_name': 'Block'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response2.status_code, 200)

        #create battle
        response3 = self.client.post('/battle/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response3.status_code, 201)

        response4 = self.client.get('/battle/' + str(self.user_id) + '/get_state/', HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response4.status_code, 200)

        # test target out of bounds
        response5 = self.client.post('/battle/' + str(self.user_id) + '/play_card/', {'id': self.user_id, 'card_name': 'Strike', 'target': 3}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response5.status_code, 404)

        response6 = self.client.post('/battle/' + str(self.user_id) + '/play_card/', {'id': self.user_id, 'card_name': 'Strike', 'target': 1}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response6.status_code, 200)

    def test_simulate_battle_out_of_mana(self):
        # Add strike card to deck
        response1 = self.client.post('/game/' + str(self.user_id) + '/add_card_to_deck/', {'card_name': 'Strike'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response1.status_code, 200)
        self.client.post('/game/' + str(self.user_id) + '/add_card_to_deck/', {'card_name': 'Strike'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.client.post('/game/' + str(self.user_id) + '/add_card_to_deck/', {'card_name': 'Strike'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))

        #create battle
        response2 = self.client.post('/battle/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response2.status_code, 201)

        response3 = self.client.post('/battle/' + str(self.user_id) + '/play_card/', {'id': self.user_id, 'card_name': 'Strike', 'target': 1}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response3.status_code, 200)

        response4 = self.client.post('/battle/' + str(self.user_id) + '/play_card/', {'id': self.user_id, 'card_name': 'Strike', 'target': 1}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response4.status_code, 200)

        response5 = self.client.post('/battle/' + str(self.user_id) + '/play_card/', {'id': self.user_id, 'card_name': 'Strike', 'target': 1}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response5.status_code, 200)

        response_state = self.client.get('/battle/' + str(self.user_id) + '/get_state/', HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        # print(response_state.data)
        enemy = json.loads(response_state.data['enemies'][0])
        self.assertEqual(enemy['enemy_name'], 'Slime')
        self.assertEqual(enemy['curr_health'], 2)

        #Out of mana fail
        response6 = self.client.post('/battle/' + str(self.user_id) + '/play_card/', {'id': self.user_id, 'card_name': 'Strike', 'target': 1}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response6.status_code, 409)

    
    def test_simulate_battle_kill_rat(self):
        # Add strike card to deck
        response1 = self.client.post('/game/' + str(self.user_id) + '/add_card_to_deck/', {'card_name': 'Strike'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response1.status_code, 200)
        self.client.post('/game/' + str(self.user_id) + '/add_card_to_deck/', {'card_name': 'Strike'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.client.post('/game/' + str(self.user_id) + '/add_card_to_deck/', {'card_name': 'Strike'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))

        #create battle
        response2 = self.client.post('/battle/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response2.status_code, 201)

        response3 = self.client.post('/battle/' + str(self.user_id) + '/play_card/', {'id': self.user_id, 'card_name': 'Strike', 'target': 2}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response3.status_code, 200)
        self.client.post('/battle/' + str(self.user_id) + '/play_card/', {'id': self.user_id, 'card_name': 'Strike', 'target': 2}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        response_state = self.client.get('/battle/' + str(self.user_id) + '/get_state/', HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(len(response_state.data['enemies']), 2)

        self.client.post('/battle/' + str(self.user_id) + '/play_card/', {'id': self.user_id, 'card_name': 'Strike', 'target': 2}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))

        response_state = self.client.get('/battle/' + str(self.user_id) + '/get_state/', HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(len(response_state.data['enemies']), 1)
        # self.assertEqual(response_state.data, assert_state)