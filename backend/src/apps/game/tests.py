import unittest
from django.test import TestCase, Client

from .main.models import Game

class GameTests(TestCase):
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

    def test_create_game(self):
        # Create game
        response1 = self.client.post('/game/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response1.status_code, 200)

    def test_add_remove_card(self):
        # Create game
        response1 = self.client.post('/game/', {'id': self.user_id}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response1.status_code, 200)

        #Add Strike to deck
        response2 = self.client.post('/game/' + str(self.user_id) + '/add_card_to_deck/', {'card_name': 'Strike'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response2.status_code, 200)

        deck_response_before = self.client.get('/game/' + str(self.user_id) + '/get_deck/', HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        deck_before = deck_response_before.data

        #Add Block to deck
        response3 = self.client.post('/game/' + str(self.user_id) + '/add_card_to_deck/', {'card_name': 'Block'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response3.status_code, 200)

        #Remove card from deck
        response4 = self.client.post('/game/' + str(self.user_id) + '/remove_card_from_deck/', {'card_name': 'Block'}, HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        self.assertEqual(response4.status_code, 200)

        deck_response_after = self.client.get('/game/' + str(self.user_id) + '/get_deck/', HTTP_AUTHORIZATION = 'JWT {}'.format(self.token))
        deck_after = deck_response_after.data
        self.assertEqual(deck_before, deck_after)

        