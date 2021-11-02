import json
import unittest
from unittest import mock
from unittest.mock import MagicMock

from assertpy import assert_that
from django.test import Client

from security.service import LoginService


class LoginViewTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @mock.patch.object(LoginService, 'authenticate')
    def test_login_with_correct_login_info(self, authenticate):
        authenticate.return_value = "access_token"
        response = self.client.post(
            "/security",
            data=json.dumps({
                "username": "asd",
                "password": "123qwe"
            }),
            content_type="application/json"
        )

        assert_that(response.status_code).is_equal_to(200)

        content = json.loads(response.content)
        assert_that(content['access_token']).is_equal_to("access_token")
