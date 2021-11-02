from dataclasses import dataclass
from typing import Optional


@dataclass
class PostChanges:
    id: int
    title: Optional['str']
    content: Optional['str']
