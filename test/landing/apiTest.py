from unittest import TestCase
from unittest.mock import patch
from src.app import app
import os

MAIN_URL = "http://localhost/vHub/"


class LandingTestCase(TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_vHub_index_returned(self):
        result = self.client.get('/vHub/')
        self.assertEqual(200, result.status_code)
        self.assertTrue(result.response is not None)

    @patch('src.landing.api.get_permissions', return_value=['write', 'read'])
    def test_apps(self, mocked_perms):
        result = self.client.get('/vHub/apps')
        self.assertEqual(200, result.status_code)
        self.assertTrue(result.json.get('success'))
        self.assertEqual(['write', 'read'], result.json.get('permissions'))

    def test_tokenAuth_redirect_url_to_vHub_Main(self):
        result = self.client.get('/vHub/tokenAuth?token=abcd')
        self.assertEqual(302,result.status_code)
        cookie = result.headers.get('Set-Cookie')
        self.assertTrue(cookie.startswith('session='))
        self.assertEqual(MAIN_URL, result.headers.get("Location"))

    def test_logout_redirect_url_to_auth0_logout(self):
        result = self.client.get('/vHub/logout')
        self.assertEqual(302, result.status_code)
        expected_url = "https://" + os.environ.get('AUTH0_URL') + '/v2/logout?returnTo=' + os.environ.get('WEB_HOST')\
            + "&client_id=" + os.environ.get('CLIENT_ID')
        self.assertEqual(expected_url, result.headers.get("Location"))
