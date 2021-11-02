import unittest
from datetime import datetime
from unittest import mock

from assertpy import assert_that

from ..dto.deleted_post_id import DeletedPostId
from ..dto.post_changes import PostChanges
from ..dto.post_content import PostContents
from ..dto.post_details import PostDetails
from ..dto.post_list import PostList
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

    @mock.patch.object(Posting, "get_by_id")
    def test_details_with_exist_posting(self, get_by_id):
        author = Member(
            username="asd",
            password="123qwe"
        )
        returned = Posting(
            id=1,
            member=author,
            title="before title",
            content="before content",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            comments=[],
            hits=0
        )
        get_by_id.return_value = returned

        actual = self.post_service.details(post_id=returned.id)
        expected = PostDetails(
            id=1,
            author=returned.member.username,
            title="before title",
            content="before content",
            created_at=returned.created_at.strftime("%m-%d-%Y, %H:%M:%S"),
            updated_at=returned.updated_at.strftime("%m-%d-%Y, %H:%M:%S"),
            comments=[],
            hits=0
        )

        assert_that(actual).is_equal_to(expected)

    @mock.patch.object(Posting, "get_partial")
    def test_post_list_with_limit_and_offset(self, get_partial):
        limit = 10
        offset = 0

        author1 = Member(
            username="qweads",
            password="123qwe"
        )
        author2 = Member(
            username="asdwqe",
            password="123qwe"
        )

        posts = [
            Posting(
                id=1,
                member=author1,
                title="before title",
                content="before content",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                comments=[],
                hits=0
            ),
            Posting(
                id=2,
                member=author2,
                title="before title",
                content="before content",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                comments=[],
                hits=0
            )
        ]
        get_partial.return_value = posts

        actual = self.post_service.list(offset=offset, limit=limit)
        expected = PostList(
            posts=[
                PostDetails(
                    id=1,
                    author="qweads",
                    title="before title",
                    content="before content",
                    created_at=posts[0].created_at.strftime("%m-%d-%Y, %H:%M:%S"),
                    updated_at=posts[0].updated_at.strftime("%m-%d-%Y, %H:%M:%S"),
                    comments=[],
                    hits=0
                ),
                PostDetails(
                    id=2,
                    author="asdwqe",
                    title="before title",
                    content="before content",
                    created_at=posts[1].created_at.strftime("%m-%d-%Y, %H:%M:%S"),
                    updated_at=posts[1].updated_at.strftime("%m-%d-%Y, %H:%M:%S"),
                    comments=[],
                    hits=0
                )
            ])

        assert_that(actual).is_equal_to(expected)
