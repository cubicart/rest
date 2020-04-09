import unittest
import requests


class TestAdminUser(unittest.TestCase):

    def test_create_user(self):
        payload = {
            'username': 'user2',
            'password': '123456',
            'first_name': 'First1',
            'last_name': 'Last1',
        }

        r = requests.post(
            'http://127.0.0.1:8000/api/v1/admin/users', json=payload)

        print(r.content)

        assert r.status_code == 201
