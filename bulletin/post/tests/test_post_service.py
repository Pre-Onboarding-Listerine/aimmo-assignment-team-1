import unittest
from datetime import datetime
from unittest import mock

from ..dto.deleted_post_id import DeletedPostId
from ..dto.post_changes import PostChanges
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

    @mock.patch.object(Posting, "save")
    @mock.patch.object(Posting, "get_by_id")
    def test_edit_with_author(self, get_by_id, save):
        updater = Member(
            username="asd",
            password="123qwe"
        )
        get_by_id.return_value = Posting(
            id=1,
            member=updater,
            title="before title",
            content="before content",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            comments=[],
            hits=0
        )

        changes = PostChanges(
            id=1,
            title="json title",
            content="qweadswqead"
        )
        self.post_service.edit(changes, updater)
        save.assert_called_with()

    @mock.patch.object(Posting, "delete")
    @mock.patch.object(Posting, "get_by_id")
    def test_remove_with_author(self, get_by_id, delete):
        deleter = Member(
            username="asd",
            password="123qwe"
        )
        deleted_post_id = DeletedPostId(
            id=1
        )
        get_by_id.return_value = Posting(
            id=1,
            member=deleter,
            title="before title",
            content="before content",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            comments=[],
            hits=0
        )
        self.post_service.remove(deleted_post_id, deleter)
        delete.assert_called_with()


