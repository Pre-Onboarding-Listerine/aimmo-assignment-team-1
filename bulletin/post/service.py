from datetime import datetime
from typing import Optional

from .dto.deleted_post_id import DeletedPostId
from .dto.list_params import ListParams
from .dto.post_changes import PostChanges
from .dto.post_content import PostContents
from member.models import Member

from .dto.post_list import PostList
from .exceptions import PostNotFoundException
from .models.posting import Posting
from security.exceptions import UnauthorizedException


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
            raise PostNotFoundException
        if posting.member != updater:
            raise UnauthorizedException
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

    def remove(self, deleted_post_id: DeletedPostId, deleter: Member):
        target = Posting.get_by_id(post_id=deleted_post_id.id)
        if target is None:
            raise PostNotFoundException
        if target.member != deleter:
            raise UnauthorizedException
        target.delete()

    def details(self, post_id: int, member: Optional[Member]):
        target = Posting.get_by_id(post_id=post_id)
        if target is None:
            raise PostNotFoundException
        if member not in target.hit_members:
            target.hits += 1
            if member:
                target.hit_members.append(member)
            target.member.save()
            target.save()
        return target.to_details()

    def list(self, params: ListParams):
        postings = Posting.get_partial(params)
        return PostList(posts=[posting.to_details() for posting in postings])
