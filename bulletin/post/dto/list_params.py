from dataclasses import dataclass
from typing import Optional


@dataclass
class ListParams:
    limit: int
    offset: int
    category: Optional[str] = None
    keyword: Optional[str] = None

    def to_filter(self):
        return {
            "category": self.category,
            "content__icontains": self.keyword
        }
