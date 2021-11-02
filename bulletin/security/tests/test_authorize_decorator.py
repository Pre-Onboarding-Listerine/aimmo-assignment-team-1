import unittest
from unittest import mock

import jwt
from assertpy import assert_that
from django.conf import settings
from django.http import HttpRequest

from ..service import authorize, general_authorize
from member.models import Member
from member.service import MemberService


class Dummy:
    @authorize
    def func(self, request, member):
        return member


class GeneralDummy:
    @general_authorize
    def func(self, request, member):
        return member


class AuthorizeServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.decorated = Dummy().func
        self.general_decorated = GeneralDummy().func

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

    @mock.patch.object(MemberService, 'get_member')
    def test_general_authorize_with_empty_authorization(self, get_member):
        get_member.return_value = Member(
            username="asd",
            password="123qwe"
        )
        request = HttpRequest()
        member = self.general_decorated(request)

        assert_that(member).is_equal_to(None)


