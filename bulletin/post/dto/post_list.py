from dataclasses import dataclass
from typing import List

from .post_details import PostDetails


@dataclass
class PostList:
    posts: List[PostDetails]

    def to_dict(self):
        return {
            "posts": [post.to_dict() for post in self.posts]
        }
