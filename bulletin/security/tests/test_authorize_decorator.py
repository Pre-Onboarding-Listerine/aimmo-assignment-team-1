import unittest
from unittest import mock

import jwt
from assertpy import assert_that
from django.conf import settings
from django.http import HttpRequest

from ..service import AuthorizationService
from member.models import Member
from member.service import MemberService


class AuthorizeServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        class Dummy:
            @AuthorizationService
            def func(self, request, member):
                return member
        self.decorated = Dummy().func

    @mock.patch.object(MemberService, 'get_member')
    def test_authorize_with_correct_jwt(self, get_member):
        get_member.return_value = Member(
            username="asd",
            password="123qwe"
        )
        request = HttpRequest()
        request.META["HTTP_Authorization"] = "Bearer " + jwt.encode(
                payload={
                    "username": "asd"
                },
                key=settings.JWT_SECRET,
                algorithm=settings.JWT_ALGORITHM
            )
        member = self.decorated(request)

        assert_that(member.username).is_equal_to("asd")
        assert_that(member.password).is_equal_to("123qwe")


