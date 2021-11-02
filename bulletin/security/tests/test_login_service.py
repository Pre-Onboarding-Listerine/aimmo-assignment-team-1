import os
import unittest
from unittest import mock

import jwt
from assertpy import assert_that
from django.conf import settings

from ..dto.login_info import LoginInfo
from ..service import LoginService
from member.service import MemberService
from member.models import Member

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bulletin.bulletin.settings")


class LoginServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = LoginService()

    @mock.patch.object(MemberService, 'get_member')
    def test_authenticate_with_correct_login_info(self, get_member):
        get_member.return_value = Member(
            username="asd",
            password="123qwe"
        )
        login_info = LoginInfo(
            username="asd",
            password="123qwe"
        )
        access_token = self.service.authenticate(login_info)
        expected = jwt.encode(
            payload={"username": "asd"},
            key=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        assert_that(access_token).is_equal_to(expected)
