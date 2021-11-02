from dataclasses import dataclass
from typing import List

from ..models.comment import Comment


@dataclass
class PostDetails:
    id: int
    author: str
    title: str
    category: str
    content: str
    created_at: str
    updated_at: str
    comments: List[Comment]
    hits: int

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "comments": self.comments,
            "hits": self.hits
        }
