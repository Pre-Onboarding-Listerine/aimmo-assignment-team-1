from dataclasses import dataclass
from typing import Optional


@dataclass
class ListParams:
    limit: int
    offset: int
    category: Optional[str] = None

    def to_filter(self):
        return {
            "category": self.category
        }
