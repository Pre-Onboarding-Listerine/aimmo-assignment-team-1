import json
import unittest
from http import HTTPStatus
from unittest import mock
from unittest.mock import MagicMock

import jwt
from assertpy import assert_that
from django.conf import settings
from django.test import Client

from member.models import Member

from ..dto.deleted_post_id import DeletedPostId
from ..dto.post_changes import PostChanges
from ..dto.post_content import PostContents
from ..service import PostService
from member.service import MemberService


class PostViewTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @mock.patch.object(MemberService, 'get_member')
    @mock.patch.object(PostService, 'write')
    def test_create_post_with_post_contents(self, write, get_member):
        get_member.return_value = Member(
            username="asd",
            password="123qwe"
        )
        access_token = "Bearer " + jwt.encode(
            payload={
                "username": "asd"
            },
            key=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        headers = {"HTTP_Authorization": access_token}

        response = self.client.post(
            "/posts",
            data=json.dumps({
                "title": "json title",
                "content": "json content"
            }),
            content_type="application/json",
            **headers
        )

        assert_that(response.status_code).is_equal_to(HTTPStatus.CREATED)
        write.assert_called_with(
            PostContents(
                title="json title",
                content="json content"
            ),
            Member(
                username="asd",
                password="123qwe"
            )
        )

    @mock.patch.object(PostService, 'edit')
    @mock.patch.object(MemberService, 'get_member')
    def test_update_post_with_author(self, get_member, edit):
        get_member.return_value = Member(
            username="asd",
            password="123qwe"
        )
        access_token = "Bearer " + jwt.encode(
            payload={
                "username": "asd"
            },
            key=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        headers = {"HTTP_Authorization": access_token}

        response = self.client.patch(
            "/posts",
            data=json.dumps({
                "id": 1,
                "title": "json title",
                "content": "json content"
            }),
            content_type="application/json",
            **headers
        )

        assert_that(response.status_code).is_equal_to(HTTPStatus.OK)

        changes = PostChanges(
            id=1,
            title="json title",
            content="json content"
        )
        updater = Member(
            username="asd",
            password="123qwe"
        )
        edit.assert_called_with(changes, updater)

    @mock.patch.object(PostService, 'remove')
    @mock.patch.object(MemberService, 'get_member')
    def test_delete_with_author(self, get_member, remove):
        get_member.return_value = Member(
            username="asd",
            password="123qwe"
        )
        access_token = "Bearer " + jwt.encode(
            payload={
                "username": "asd"
            },
            key=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        headers = {"HTTP_Authorization": access_token}

        response = self.client.delete(
            "/posts",
            data=json.dumps({
                "id": 1
            }),
            content_type="application/json",
            **headers
        )
        assert_that(response.status_code).is_equal_to(HTTPStatus.NO_CONTENT)

        deleted_post_id = DeletedPostId(
            id=1
        )
        deleter = Member(
            username="asd",
            password="123qwe"
        )
        remove.assert_called_with(deleted_post_id, deleter)




