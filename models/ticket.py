# generated by datamodel-codegen:
#   filename:  <stdin>
#   timestamp: 2022-06-28T21:26:22+00:00
from typing import List
from pydantic import BaseModel

from models.event import Event


class Ticket(BaseModel):
    price: float
    name: str
    lowest_price: float
    available_tickets_count: int
    location: str
    url: str
    created_at: str


def extract_tickets(events: List[Event]) -> List[Ticket]:
    result: List[Ticket] = []

    for event in events:
        lowest_price: float = event.lowest_price.amount / 100
        available_tickets_count = event.available_tickets_count
        start_date = event.start_date
        end_date = event.end_date
        location = event.location.name
        for edge in event.types.edges:
            for listing_edge in edge.node.available_listings.edges:
                url = listing_edge.node.uri.url
                price = (
                    listing_edge.node.price.total_price_with_transaction_fee.amount
                    / 100
                )
                created_at = listing_edge.node.created_at
                res = dict(
                    price=price,
                    name=event.name,
                    lowest_price=lowest_price,
                    available_tickets_count=available_tickets_count,
                    location=location,
                    url=url,
                    created_at=created_at,
                )
                result.append(Ticket(**res))

    return result
