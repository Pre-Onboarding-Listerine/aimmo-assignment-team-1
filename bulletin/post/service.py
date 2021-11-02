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
