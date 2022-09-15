from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel, Field


class Tags(BaseModel):
    edges: List
    __typename: str


class SeoMetadata(BaseModel):
    title: Any
    description: Any
    __typename: str


class SecureSwapInformation(BaseModel):
    is_manual_secure_swap_available: bool = Field(
        ..., alias='isManualSecureSwapAvailable'
    )
    __typename: str


class GeoInfo(BaseModel):
    latitude: Any
    longitude: Any
    __typename: str


class City(BaseModel):
    id: str
    slug: str
    name: str
    __typename: str


class Country(BaseModel):
    name: str
    code: str
    __typename: str


class Location(BaseModel):
    id: str
    slug: str
    name: str
    geo_info: GeoInfo = Field(..., alias='geoInfo')
    background: Any
    amount_of_active_upcoming_events: int = Field(
        ..., alias='amountOfActiveUpcomingEvents'
    )
    image: Any
    website: Any
    average_fan_experience_rating: int = Field(..., alias='averageFanExperienceRating')
    total_amount_of_fan_experiences: int = Field(
        ..., alias='totalAmountOfFanExperiences'
    )
    city: City
    country: Country
    __typename: str


class Node1(BaseModel):
    id: str
    slug: str
    title: str
    available_tickets_count: int = Field(..., alias='availableTicketsCount')
    __typename: str


class Edge(BaseModel):
    node: Node1
    __typename: str


class Types(BaseModel):
    edges: List[Edge]
    __typename: str


class Country1(BaseModel):
    code: str
    __typename: str


class Node2(BaseModel):
    id: str
    slug: str
    title: str
    start_date: str = Field(..., alias='startDate')
    end_date: Any = Field(..., alias='endDate')
    is_ongoing: bool = Field(..., alias='isOngoing')
    available_tickets_count: int = Field(..., alias='availableTicketsCount')
    is_selling_blocked: bool = Field(..., alias='isSellingBlocked')
    __typename: str


class Edge1(BaseModel):
    node: Node2
    __typename: str


class EntranceTypes(BaseModel):
    edges: List[Edge1]
    __typename: str


class NonEntranceTypesWithoutGroup(BaseModel):
    edges: List
    __typename: str


class OriginalPrice(BaseModel):
    amount: int
    currency: str
    __typename: str


class Price(BaseModel):
    original_price: OriginalPrice = Field(..., alias='originalPrice')
    __typename: str


class Seller(BaseModel):
    id: str
    avatar: str
    __typename: str


class Node3(BaseModel):
    id: str
    price: Price
    seller: Seller
    __typename: str


class Edge2(BaseModel):
    node: Node3
    __typename: str


class AvailableListings(BaseModel):
    edges: List[Edge2]
    __typename: str


class Seller1(BaseModel):
    id: str
    avatar: str
    __typename: str


class Node4(BaseModel):
    id: str
    seller: Seller1
    __typename: str


class Edge3(BaseModel):
    node: Node4
    __typename: str


class SoldListings(BaseModel):
    edges: List[Edge3]
    __typename: str


class EventDataResponse(BaseModel):
    id: str
    slug: str
    name: str
    status: str
    is_event_favorited_by_user: bool = Field(..., alias='isEventFavoritedByUser')
    is_selling_blocked: bool = Field(..., alias='isSellingBlocked')
    is_buying_blocked: bool = Field(..., alias='isBuyingBlocked')
    is_popular: bool = Field(..., alias='isPopular')
    category: Any
    time_zone: str = Field(..., alias='timeZone')
    instagram_username: Any = Field(..., alias='instagramUsername')
    start_date: str = Field(..., alias='startDate')
    end_date: Any = Field(..., alias='endDate')
    has_ongoing_event_type: bool = Field(..., alias='hasOngoingEventType')
    tags: Tags
    facebook_event_walls: List = Field(..., alias='facebookEventWalls')
    is_verified: bool = Field(..., alias='isVerified')
    seo_metadata: SeoMetadata = Field(..., alias='seoMetadata')
    description: Any
    event_video: Any = Field(..., alias='eventVideo')
    closed_loop_information: Any = Field(..., alias='closedLoopInformation')
    secure_swap_information: SecureSwapInformation = Field(
        ..., alias='secureSwapInformation'
    )
    alias: Any
    header_image_url: Any = Field(..., alias='headerImageUrl')
    image_url: str = Field(..., alias='imageUrl')
    image_small_url: Any = Field(..., alias='imageSmallUrl')
    organizer_shop: Any = Field(..., alias='organizerShop')
    location: Location
    organizer_brands: List = Field(..., alias='organizerBrands')
    artists: List
    types: Types
    warning: Any
    __typename: str
    available_tickets_count: int = Field(..., alias='availableTicketsCount')
    sold_tickets_count: int = Field(..., alias='soldTicketsCount')
    ticket_alerts_count: int = Field(..., alias='ticketAlertsCount')
    cancellation_reason: Any = Field(..., alias='cancellationReason')
    is_highlighted: bool = Field(..., alias='isHighlighted')
    country: Country1
    entrance_types: EntranceTypes = Field(..., alias='entranceTypes')
    non_entrance_types_without_group: NonEntranceTypesWithoutGroup = Field(
        ..., alias='nonEntranceTypesWithoutGroup'
    )
    event_type_groups: List = Field(..., alias='eventTypeGroups')
    redirected_to: Any = Field(..., alias='redirectedTo')
    available_listings: AvailableListings = Field(..., alias='availableListings')
    sold_listings: SoldListings = Field(..., alias='soldListings')
    external_primary_ticket_shops: List = Field(..., alias='externalPrimaryTicketShops')
