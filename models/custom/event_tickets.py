""" Wrapper class to parse GraphQL JSON response and return custom 'TicketsForSale' instance"""
from datetime import datetime
import json
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from models.rest.tickets import TicketswapTickets

BASE_URL = 'http://ticketswap.com'


class TicketForSale(BaseModel):
    updated: datetime = Field(default_factory=datetime.utcnow)
    id: str
    event_name: str
    event_start_date: str
    event_end_date: Optional[str]
    amount_of_tickets: int
    entrance_slug: str
    original_price: float
    price: float
    location: str
    city: str
    url: str


class TicketSold(BaseModel):
    updated: datetime = Field(default_factory=datetime.utcnow)
    id: str


class EventTickets(BaseModel):
    tickets_for_sale: Optional[List[TicketForSale]]
    tickets_sold: Optional[List[TicketSold]]
    entrance_slug: str
    name: str
    start_date: str
    end_date: Optional[str]
    city: str
    location: str

    def __init__(self, **data):
        event_tickets: TicketswapTickets = TicketswapTickets(**data)

        event_name = event_tickets.page_props.initial_apollo_state.active_event.name
        data["name"] = event_name

        event_start_date = (
            event_tickets.page_props.initial_apollo_state.active_event.start_date
        )
        data["start_date"] = event_start_date

        event_end_date = (
            event_tickets.page_props.initial_apollo_state.active_event.end_date
        )
        data["end_date"] = event_end_date

        event_type_slug = event_tickets.page_props.event_type_slug
        data["entrance_slug"] = event_type_slug

        city = event_tickets.page_props.initial_apollo_state.city
        data["city"] = city

        location = event_tickets.page_props.initial_apollo_state.location
        data["location"] = location

        tickets_for_sale = []
        try:
            for (
                public_listing
            ) in event_tickets.page_props.initial_apollo_state.public_listings:
                original_price = float(public_listing.price.original_price.amount / 100)
                price = float(
                    public_listing.price.total_price_with_transaction_fee.amount / 100
                )
                ticket_for_sale = TicketForSale(
                    id=public_listing.id,
                    amount_of_tickets=public_listing.number_of_tickets_still_for_sale,
                    original_price=original_price,
                    price=price,
                    event_start_date=event_start_date,
                    event_end_date=event_end_date,
                    event_name=event_name,
                    entrance_slug=event_type_slug,
                    location = location,
                    city=city,
                    url= BASE_URL + public_listing.uri.path
                )

                tickets_for_sale.append(ticket_for_sale)
            data["tickets_for_sale"] = tickets_for_sale
        except AttributeError as e:
            print(e)

        super().__init__(**data)


class EventTicketsParser:
    event_tickets: List[EventTickets] = []

    def parse(self, event_tickets_json: Dict):
        self.event_tickets.append(EventTickets(**event_tickets_json))

    def store_available_tickets(self, path: str):
        all_tickets_for_sale: List[Dict[str, str]] = []
        for event in self.event_tickets:
            for ticket in event.tickets_for_sale:
                all_tickets_for_sale.append(ticket.dict())

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {"tickets_for_sale": all_tickets_for_sale},
                f,
                ensure_ascii=False,
                indent=4,
                default=str
            )
