from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class APIRootTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_root(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expected_keys = {'teams', 'users', 'activities', 'workouts', 'leaderboard'}
        self.assertTrue(expected_keys.issubset(set(resp.data.keys())))

    def test_get_teams_list(self):
        resp = self.client.get('/api/teams/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
