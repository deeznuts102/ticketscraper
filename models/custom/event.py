
""" Wrapper class to parse GraphQL JSON response and return custom 'TicketsForSale' instance"""
from typing import List, Optional

from pydantic import BaseModel

from models.custom.event_entrance_type import EventEntranceType

class Event(BaseModel):
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
