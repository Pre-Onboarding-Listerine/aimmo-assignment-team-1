import json
import unittest
from http import HTTPStatus
from unittest import mock

from assertpy import assert_that
from django.test import Client

from ..dto.signup_info import SignUpInfo
from ..service import MemberService


class SignUpViewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Client()

    @mock.patch.object(MemberService, 'add_member')
    def test_sign_up_with_correct_correct_sign_up_info(self, add_member):
        response = self.client.post(
            "/members",
            data=json.dumps({
                "username": "asd",
                "password": "123qwe"
            }),
            content_type="application/json"
        )

        assert_that(response.status_code).is_equal_to(HTTPStatus.CREATED)
        add_member.assert_called_with(
            SignUpInfo(
                username="asd",
                password="123qwe"
            )
        )
