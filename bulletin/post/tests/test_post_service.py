import unittest
from unittest import mock

from ..dto.post_content import PostContents
from ..models.posting import Posting
from ..service import PostService
from member.models import Member


class PostServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.post_service = PostService()

    @mock.patch.object(Posting, "add")
    def test_write_with_correct_post_content(self, add):
        author = Member(
            username="asdf",
            password="123qwe"
        )
        contents = PostContents(
            title="json title",
            content="json content"
        )

        self.post_service.write(contents, author)
        new_posting = Posting(
            member=author,
            title=contents.title,
            content=contents.content
        )

        add.assert_called_with(new_posting)

