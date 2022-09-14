from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel, Field

class EntranceTypeNode(BaseModel):
    __typename: str
    slug: str
    title: str
    start_date: str = Field(..., alias='startDate')
    end_date: str = Field(..., alias='endDate')
    available_tickets_count: int = Field(..., alias='availableTicketsCount')

class EntranceTypeEdges(BaseModel):
    node: EntranceTypeNode


class EntranceTypes(BaseModel):
    edges: List[EntranceTypeEdges]


class Event(BaseModel):
    available_tickets_count: int = Field(..., alias='availableTicketsCount')
    sold_tickets_count: int = Field(..., alias='soldTicketsCount')
    ticket_alerts_count: int = Field(..., alias='ticketAlertsCount')
    entrance_types: EntranceTypes = Field(..., alias='entranceTypes')
    name: str
    status: str
    is_event_favorited_by_user: bool = Field(..., alias='isEventFavoritedByUser')
    is_popular: bool = Field(..., alias='isPopular')
    start_date: str = Field(..., alias='startDate')
    end_date: str = Field(..., alias='endDate')
    description: Any

class PageProps(BaseModel):
    event_id: str = Field(..., alias='eventId')
    event: Event
    event_slug: str = Field(..., alias='eventSlug')
    theme: Any
    random_cover: str = Field(..., alias='randomCover')
    current_url: str = Field(..., alias='currentUrl')
    enabled_beta_features: List = Field(..., alias='enabledBetaFeatures')

class EntranceType(BaseModel):
    slug: str
    available_tickets: int
    start_date: str
    end_date: str
    event_slug: str
    event_available_tickets: int
    event_sold_tickets: int
    event_wanted_tickets: int


class EventInfo(BaseModel):
    """ Tickets model returned by the Ticketswap REST API"""
    page_props: PageProps = Field(..., alias='pageProps')

    def get_entrance_types(self) -> List[EntranceType]:
        entrance_types: List[EntranceType] = []

        try:
            for edge in self.page_props.event.entrance_types.edges:  # type: ignore
                entrance_type = EntranceType(
                    slug=edge.node.slug,
                    available_tickets=edge.node.available_tickets_count,
                    start_date=edge.node.start_date,
                    end_date=edge.node.end_date,
                    event_slug=self.page_props.event_slug,
                    event_available_tickets=self.page_props.event.available_tickets_count,
                    event_sold_tickets=self.page_props.event.sold_tickets_count,
                    event_wanted_tickets=self.page_props.event.ticket_alerts_count
                )

                entrance_types.append(entrance_type)
        except AttributeError as e:
            print(e)

        return entrance_types