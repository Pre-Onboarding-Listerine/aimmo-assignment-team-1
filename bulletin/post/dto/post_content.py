from dataclasses import dataclass


@dataclass
class PostContents:
    title: str
    category: str
    content: str
