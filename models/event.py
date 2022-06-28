# generated by datamodel-codegen:
#   filename:  2022-06-27.json
#   timestamp: 2022-06-28T20:16:03+00:00


from typing import Any, Optional
from pydantic import BaseModel, Field


class TotalPriceWithTransactionFee(BaseModel):
    id: Any
    amount: int
    currency: str
    __typename: str


class Price(BaseModel):
    total_price_with_transaction_fee: TotalPriceWithTransactionFee = Field(
        ..., alias="totalPriceWithTransactionFee"
    )
    __typename: str


class Uri(BaseModel):
    url: str
    __typename: str


class Node1(BaseModel):
    price: Price
    id: str
    uri: Uri
    __typename: str
    created_at: str = Field(..., alias="createdAt")


class Edge1(BaseModel):
    node: Node1
    id: Any
    __typename: str


class AvailableListings(BaseModel):
    edges: list[Edge1]
    __typename: str


class Node(BaseModel):
    id: str
    available_listings: AvailableListings = Field(..., alias="availableListings")
    __typename: str


class Edge(BaseModel):
    node: Node
    __typename: str


class Types(BaseModel):
    edges: list[Edge]
    __typename: str


class Uri1(BaseModel):
    url: str
    __typename: str


class LowestPrice(BaseModel):
    amount: int
    currency: str
    __typename: str


class OrganizerBrand(BaseModel):
    id: str
    name: str
    __typename: str


class Artist(BaseModel):
    id: str
    name: str
    __typename: str


class Uri2(BaseModel):
    url: str
    __typename: str


class City(BaseModel):
    id: str
    name: str
    __typename: str


class Country(BaseModel):
    name: str
    code: str
    __typename: str


class Location(BaseModel):
    id: str
    uri: Uri2
    address: Optional[str]
    zipcode: Optional[str]
    name: str
    city: City
    country: Country
    __typename: str


class Event(BaseModel):
    id: str
    types: Types
    prices: Optional[list[float]]
    uri: Uri1
    lowest_price: LowestPrice = Field(..., alias="lowestPrice")
    organizer_brands: list[OrganizerBrand] = Field(..., alias="organizerBrands")
    start_date: str = Field(..., alias="startDate")
    artists: list[Artist]
    end_date: Optional[str] = Field(..., alias="endDate")
    name: str
    available_tickets_count: int = Field(..., alias="availableTicketsCount")
    location: Location
    status: str
    __typename: str