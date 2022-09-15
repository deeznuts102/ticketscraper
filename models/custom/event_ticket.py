from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EventTicketForSale(BaseModel):
    updated: datetime = Field(default_factory=datetime.utcnow)
    id: str
    description: Optional[str]
    event_name: str
    event_start_date: str
    event_end_date: Optional[str]
    amount_of_tickets: int
    entrance_slug: str
    entrance_id: str
    original_price: float
    price: float
    location: str
    city: str
    url: str


class EventTicketSold(BaseModel):
    updated: datetime = Field(default_factory=datetime.utcnow)
    id: str
    description: Optional[str]
    event_name: str
    event_start_date: str
    event_end_date: Optional[str]
    amount_of_tickets: int
    entrance_title: str
    entrance_id: str
    original_price: float
    price: float
    location: str
    city: str
    url: str
