import os
import unittest
from unittest import mock

from assertpy import assert_that

from ..models import Member
from ..service import MemberService


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bulletin.bulletin.settings")


class MemberServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = MemberService()

    @mock.patch.object(Member, 'get_by_username')
    def test_get_member_with_exist_member(self, get_by_username):
        get_by_username.return_value = Member(
            username="asd",
            password="123qwe"
        )
        member = self.service.get_member("asd")
        expected = Member(
            username="asd",
            password="123qwe"
        )

        assert_that(member.username).is_equal_to(expected.username)
        assert_that(member.password).is_equal_to(expected.password)

