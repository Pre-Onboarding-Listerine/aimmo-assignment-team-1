import json
import unittest
from http import HTTPStatus

from assertpy import assert_that
from django.test import Client


class PostViewTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_post_with_post_contents(self):
        response = self.client.post(
            "/posts",
            data=json.dumps({
                "title": "json title",
                "content": "json content"
            }),
            content_type='application/json'
        )

        assert_that(response.status_code).is_equal_to(HTTPStatus.CREATED)
