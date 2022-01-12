from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Todo:
    task: str
    category: str
    date_added: datetime = None
    date_completed: datetime = None
    status: int = None
    position: int = None

    def __post_init__(self):
        self.date_added = (
            self.date_added if self.date_added is not None else datetime.now().isoformat()
        )
        self.date_completed = self.date_completed if self.date_completed is not None else None
        self.status = (
            self.status if self.status is not None else 1
        )  # NOTE: 1 = open, 2 = completed
        self.position = self.position if self.position is not None else None

    def __repr__(self) -> str:
        return (
            f"({self.task}, {self.category}, {self.date_added}, "
            f"{self.date_completed}, {self.status}, {self.position})"
        )
