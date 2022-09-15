from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Uri(BaseModel):
    path: str
    __typename: str


class City(BaseModel):
    id: str
    name: str
    __typename: str


class Location(BaseModel):
    id: str
    name: str
    city: City
    __typename: str


class Event(BaseModel):
    id: str
    name: str
    start_date: str = Field(..., alias='startDate')
    end_date: Any = Field(..., alias='endDate')
    slug: str
    status: str
    location: Location
    __typename: str


class EventType(BaseModel):
    id: str
    title: str
    start_date: str = Field(..., alias='startDate')
    end_date: Any = Field(..., alias='endDate')
    __typename: str


class Seller(BaseModel):
    id: str
    firstname: str
    avatar: str
    __typename: str


class Node1(BaseModel):
    id: str
    status: str
    __typename: str


class Edge1(BaseModel):
    node: Node1
    __typename: str


class Tickets(BaseModel):
    edges: List[Edge1]
    __typename: str


class OriginalPrice(BaseModel):
    amount: int
    currency: str
    __typename: str


class TotalPriceWithTransactionFee(BaseModel):
    amount: int
    currency: str
    __typename: str


class SellerPrice(BaseModel):
    amount: int
    currency: str
    __typename: str


class Price(BaseModel):
    original_price: OriginalPrice = Field(..., alias='originalPrice')
    total_price_with_transaction_fee: TotalPriceWithTransactionFee = Field(
        ..., alias='totalPriceWithTransactionFee'
    )
    seller_price: SellerPrice = Field(..., alias='sellerPrice')
    __typename: str


class Node(BaseModel):
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
    tickets: Tickets
    number_of_tickets_in_listing: int = Field(..., alias='numberOfTicketsInListing')
    number_of_tickets_still_for_sale: int = Field(
        ..., alias='numberOfTicketsStillForSale'
    )
    price: Price
    __typename: str


class Edge(BaseModel):
    node: Node
    __typename: str


class PageInfo(BaseModel):
    end_cursor: str = Field(..., alias='endCursor')
    has_next_page: bool = Field(..., alias='hasNextPage')
    __typename: str


class AvailableListings(BaseModel):
    edges: List[Edge]
    page_info: PageInfo = Field(..., alias='pageInfo')
    __typename: str


class EventTickets(BaseModel):
    id: str
    slug: str
    title: str
    available_listings: AvailableListings = Field(..., alias='availableListings')
    __typename: str
