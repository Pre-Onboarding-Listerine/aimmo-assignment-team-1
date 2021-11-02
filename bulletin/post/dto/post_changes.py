from dataclasses import dataclass
from typing import Optional


@dataclass
class PostChanges:
    id: int
    category: Optional[str] = None
    title: Optional['str'] = None
    content: Optional['str'] = None
