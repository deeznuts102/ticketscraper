# generated by datamodel-codegen:
#   filename:  tickets.json
#   timestamp: 2022-09-09T22:37:39+00:00

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, Extra

class ActiveEvent(BaseModel):
    id: str
    slug: str
    name: str
    category: Optional[str]
    time_zone: str = Field(..., alias='timeZone')
    start_date: str = Field(..., alias='startDate')
    end_date: Optional[str] = Field(alias='endDate')


class TicketEvent(BaseModel):
    id: str
    slug: str
    title: str
    available_tickets_count: Optional[int] = Field( alias='availableTicketsCount')
    start_date: Optional[str] = Field( alias='startDate')
    end_date: Optional[str] = Field( alias='endDate')
    is_selling_blocked: Optional[bool] = Field( alias='isSellingBlocked')
    is_ongoing: Optional[bool] = Field( alias='isOngoing')
    sold_tickets_count: Optional[int] = Field( alias='soldTicketsCount')
    ticket_alerts_count: Optional[int] = Field( alias='ticketAlertsCount')


class Uri(BaseModel):
    __typename: str
    path: str


class Event(BaseModel):
    __ref: str


class EventType(BaseModel):
    __ref: str


class Seller(BaseModel):
    __ref: str

class OriginalPrice(BaseModel):
    __typename: str
    amount: int
    currency: str


class TotalPriceWithTransactionFee(BaseModel):
    __typename: str
    amount: int
    currency: str


class SellerPrice(BaseModel):
    __typename: str
    amount: int
    currency: str


class Price(BaseModel):
    __typename: str
    original_price: OriginalPrice = Field(..., alias='originalPrice')
    total_price_with_transaction_fee: TotalPriceWithTransactionFee = Field(
        ..., alias='totalPriceWithTransactionFee'
    )
    seller_price: SellerPrice = Field(..., alias='sellerPrice')


class PublicListing(BaseModel):
    __typename: str
    id: str
    hash: str
    description: Optional[str]
    is_public: bool = Field(..., alias='isPublic')
    status: str
    date_range: Any = Field(..., alias='dateRange')
    uri: Uri
    event: Event
    event_type: EventType = Field(..., alias='eventType')
    seller: Seller
    number_of_tickets_in_listing: int = Field(..., alias='numberOfTicketsInListing')
    number_of_tickets_still_for_sale: int = Field(
        ..., alias='numberOfTicketsStillForSale'
    )
    price: Price



class InitialApolloState(BaseModel):
    event_types: Optional[List[TicketEvent]]
    public_listings: Optional[List[PublicListing]]
    active_event: Optional[ActiveEvent]
    location: str
    city: str

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow


    def __init__(self, **data):
        data['event_types'] = self.parse_ticket_events(data)
        data['public_listings'] = self.parse_public_listings(data)
        data['active_event'] = self.parse_active_event(data)
        data['location'] = self.parse_location(data)
        data['city'] = self.parse_city(data)

        super().__init__(**data)

    def parse_ticket_events(self, data: Dict) -> List[TicketEvent]:
        ticket_events = []
        for field in data:
            if 'EventType:' in field:
                event_json = data[field]
                if event_json['availableTicketsCount'] > 0:
                    event = TicketEvent(**event_json)
                    ticket_events.append(event)

        return ticket_events

    def parse_public_listings(self, data: Dict) -> List[PublicListing]:
        public_listings = []
        for field in data:
            if 'PublicListing:' in field:
                listing = PublicListing(**data[field])
                public_listings.append(listing)

        return public_listings

    def parse_active_event(self, data: Dict) -> List[PublicListing]:
        for field in data:
            if 'ActiveEvent:' in field:
                return ActiveEvent(**data[field])

    def parse_location(self, data: Dict) -> str:
        for field in data:
            if 'Location:' in field:
                return data[field]['name']

    def parse_city(self, data: Dict) -> str:
        for field in data:
            if 'City:' in field:
                return data[field]['name']

class PageProps(BaseModel):
    event_slug: str = Field(..., alias='eventSlug')
    theme: Any
    event_id: str = Field(..., alias='eventId')
    event_type_slug: str = Field(..., alias='eventTypeSlug')
    event_type_id: str = Field(..., alias='eventTypeId')
    current_url: str = Field(..., alias='currentUrl')
    initial_apollo_state: InitialApolloState = Field(..., alias='initialApolloState')


class Tickets(BaseModel):
    """ Tickets model returned by the Ticketswap GraphQL API"""
    page_props: PageProps = Field(..., alias='pageProps')
