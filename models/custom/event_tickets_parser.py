""" Wrapper class to parse GraphQL JSON response and return custom 'TicketsForSale' instance"""
from datetime import datetime
import json
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from models.graphql.sold_listings import SoldListings, SoldListingsResponse

from models.rest.tickets import Tickets

BASE_URL = "http://ticketswap.com"


class TicketForSale(BaseModel):
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


class TicketSold(BaseModel):
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


# class Event(BaseModel):
#     tickets_for_sale: Optional[List[TicketForSale]]
#     tickets_sold: Optional[List[TicketSold]]
#     entrance_slug: str
#     name: str
#     start_date: str
#     end_date: Optional[str]
#     city: str
#     location: str
#     availableTicketsCount: str
#     soldTicketsCount: str
#     ticketAlertsCount: str


class EventTicketsParser:
    tickets_for_sale: List[TicketForSale] = []
    tickets_sold: List[TicketSold] = []

    def parse_available_tickets(self, event_tickets_json: Dict):
        ticketswap_tickets: Tickets = Tickets(**event_tickets_json)

        try:
            for (
                public_listing
            ) in ticketswap_tickets.page_props.initial_apollo_state.public_listings:
                ticket_for_sale = TicketForSale(
                    id=public_listing.id,
                    description=public_listing.description,
                    amount_of_tickets=public_listing.number_of_tickets_still_for_sale,
                    original_price=self.convert_price(public_listing.price.original_price.amount),
                    price=self.convert_price(public_listing.price.total_price_with_transaction_fee.amount),
                    event_start_date=ticketswap_tickets.page_props.initial_apollo_state.active_event.start_date,
                    event_end_date=ticketswap_tickets.page_props.initial_apollo_state.active_event.end_date,
                    event_name=ticketswap_tickets.page_props.initial_apollo_state.active_event.name,
                    entrance_slug=ticketswap_tickets.page_props.event_type_slug,
                    entrance_id=ticketswap_tickets.page_props.event_type_id,
                    location=ticketswap_tickets.page_props.initial_apollo_state.location,
                    city=ticketswap_tickets.page_props.initial_apollo_state.city,
                    url=BASE_URL + public_listing.uri.path,
                )

                self.tickets_for_sale.append(ticket_for_sale)
        except AttributeError as e:
            print(e)

    def parse_sold_tickets(self, sold_listings_json: Dict):
        sold_listings_response: SoldListingsResponse = SoldListingsResponse(**sold_listings_json[0]["data"]['node'])
        try:
            for edge in sold_listings_response.sold_listings.edges:
                sold_ticket = TicketSold(
                    id=edge.node.id,
                    description=edge.node.description,
                    amount_of_tickets=edge.node.number_of_tickets_in_listing,
                    original_price=self.convert_price(
                        edge.node.price.original_price.amount
                    ),
                    price=self.convert_price(
                        edge.node.price.total_price_with_transaction_fee.amount
                    ),
                    city=edge.node.event.location.city.name,
                    location=edge.node.event.location.name,
                    entrance_title=edge.node.event_type.title,
                    entrance_id=edge.node.event_type.id,
                    event_name=edge.node.event.name,
                    event_start_date=edge.node.event.start_date,
                    event_end_date=edge.node.event.end_date,
                    url=BASE_URL + edge.node.uri.path,
                )
                self.tickets_sold.append(sold_ticket)
        except AttributeError as e:
            print(e)
    
    def get_available_entrance_ids(self) -> List[str]:
        entrance_ids = []
        for ticket in self.tickets_for_sale:
            if ticket.entrance_id not in entrance_ids:
                entrance_ids.append(ticket.entrance_id)

        return entrance_ids

    def store(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "tickets_for_sale": [
                        ticket.dict() for ticket in self.tickets_for_sale
                    ],
                    "sold_tickets": [ticket.dict() for ticket in self.tickets_sold],
                },
                f,
                ensure_ascii=False,
                indent=4,
                default=str,
            )

    def convert_price(self, price) -> float:
        """Convert price amount in cents to decimal"""
        return float(price / 100)
