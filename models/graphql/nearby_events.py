from __future__ import annotations
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class Country(BaseModel):
    name: str
    code: str


class Uri(BaseModel):
    path: str


class City(BaseModel):
    id: str
    name: str


class Location(BaseModel):
    id: str
    name: str
    city: City


class Node(BaseModel):
    id: str
    slug: str
    name: str
    is_highlighted: bool = Field(..., alias='isHighlighted')
    image_url: str = Field(..., alias='imageUrl')
    category: Optional[str]
    start_date: str = Field(..., alias='startDate')
    end_date: Optional[str] = Field(..., alias='endDate')
    available_tickets_count: int = Field(..., alias='availableTicketsCount')
    status: str
    artists: List
    country: Country
    uri: Uri
    location: Location


class Edge(BaseModel):
    node: Node


class PageInfo(BaseModel):
    end_cursor: str = Field(..., alias='endCursor')
    has_next_page: bool = Field(..., alias='hasNextPage')


class ActiveEvents(BaseModel):
    period: str
    edges: List[Edge]
    page_info: PageInfo = Field(..., alias='pageInfo')


class Data(BaseModel):
    active_events: ActiveEvents = Field(..., alias='activeEvents')

class Event(BaseModel):
    city_name: str
    id: str
    location_name: str
    name: str
    path: str
    slug: str
    uri_id: str
    uri_path: str


class NearbyEvents(BaseModel):
    data: Data

    def get_events(self) -> List[Event]:
        events: List[Event] = []

        try:
            for edge in self.data.active_events.edges:  # type: ignore
                event = Event(
                    id=edge.node.id,
                    name=edge.node.name,
                    path=edge.node.uri.path,
                    slug=edge.node.slug,
                    uri_path=edge.node.uri.path,
                    uri_id=edge.node.uri.path.split("/")[-1],
                    location_name= edge.node.location.name,
                    city_name = edge.node.location.city.name
                )

                events.append(event)
        except AttributeError as e:
            print(e)

        return events