import json
import unittest
from datetime import datetime
from http import HTTPStatus
from unittest import mock

from assertpy import assert_that
from django.test import Client

from ..dto.post_details import PostDetails
from ..dto.post_list import PostList
from ..service import PostService


class PostListViewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Client()

    @mock.patch.object(PostService, "list")
    def test_get_post_list_with_paging_info(self, list):
        post_list = PostList(
            posts=[
                PostDetails(
                    id=1,
                    author="qweads",
                    title="before title",
                    content="before content",
                    created_at=datetime.utcnow().strftime("%m-%d-%Y, %H:%M:%S"),
                    updated_at=datetime.utcnow().strftime("%m-%d-%Y, %H:%M:%S"),
                    comments=[],
                    hits=0
                ),
                PostDetails(
                    id=2,
                    author="asdwqe",
                    title="before title",
                    content="before content",
                    created_at=datetime.utcnow().strftime("%m-%d-%Y, %H:%M:%S"),
                    updated_at=datetime.utcnow().strftime("%m-%d-%Y, %H:%M:%S"),
                    comments=[],
                    hits=0
                )
            ])
        list.return_value = post_list

        response = self.client.get(
            "/posts/postings",
            data={
                "limit": 10,
                "offset": 0
            }
        )

        assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
        content = json.loads(response.content)
        expected = [
            {
                'author': 'qweads',
                'comments': [],
                'content': 'before content',
                'created_at': post_list.posts[0].created_at,
                'hits': 0,
                'id': 1,
                'updated_at': post_list.posts[0].updated_at
            },
            {
                'author': 'asdwqe',
                'comments': [],
                'content': 'before content',
                'created_at': post_list.posts[1].created_at,
                'hits': 0,
                'id': 2,
                'updated_at': post_list.posts[1].updated_at
            }
        ]
        assert_that(content['posts']).is_equal_to(expected)
