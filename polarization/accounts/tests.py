from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class NodeTestCase(TestCase):

    def test_create_node(self):
        client = APIClient()
        client.default_format = 'json'

        data = {"handle": "enisbt"}
        request = client.post('/api/nodes/')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
