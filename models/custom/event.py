
""" Wrapper class to parse GraphQL JSON response and return custom 'TicketsForSale' instance"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from models.custom.event_entrance_type import EventEntranceType

class Event(BaseModel):
    updated: datetime = Field(default_factory=datetime.utcnow)
    id: str
    entrance_slug: str
    name: str
    start_date: str
    end_date: Optional[str]
    location: str
    city: str
    available_tickets: str
    sold_tickets: str
    wanted_tickets: str
    entrance_types: List[EventEntranceType]
    url: Optional[str]
