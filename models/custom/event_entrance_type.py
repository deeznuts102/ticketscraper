from typing import List, Optional

from pydantic import BaseModel

class EventEntranceType(BaseModel):
    id: str
    slug: str
    title: str
    start_date: str
    end_date: Optional[str]
    available_tickets: int
