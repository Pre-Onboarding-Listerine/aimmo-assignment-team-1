from datetime import datetime

from .dto.post_changes import PostChanges
from .dto.post_content import PostContents
from member.models import Member

from .models.posting import Posting


class PostService:
    def write(self, contents: PostContents, author: Member):
        new_posting = Posting(
            member=author,
            title=contents.title,
            content=contents.content
        )
        Posting.add(new_posting)

    def edit(self, changes: PostChanges, updater: Member):
        posting = Posting.get_by_id(post_id=changes.id)
        if posting is None:
            # todo: PostNotFoundException
            raise Exception
        if posting.member != updater:
            # todo: Unauthorized
            raise Exception
        edited = Posting(
            id=changes.id,
            member=updater,
            title=changes.title if changes.title else posting.title,
            content=changes.content if changes.content else posting.content,
            created_at=posting.created_at,
            updated_at=datetime.utcnow(),
            comments=posting.comments,
            hits=posting.hits
        )
        edited.save()
