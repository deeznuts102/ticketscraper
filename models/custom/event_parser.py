""" Wrapper class to parse GraphQL JSON response and return custom 'TicketsForSale' instance"""
from datetime import datetime
import json
from typing import Dict, List
from models.custom.event_entrance_type import EventEntranceType
from models.custom.event_ticket import EventTicketForSale, EventTicketSold
from models.custom.event import Event

from models.graphql.sold_listings import SoldListingsResponse
from models.graphql.event_data import EventDataResponse

from models.rest.tickets import Tickets

BASE_URL = "http://ticketswap.com"


class EventParser:
    tickets_for_sale: List[EventTicketForSale] = []
    tickets_sold: List[EventTicketSold] = []
    events: List[Event] = []

    def parse_available_tickets(
        self, event_tickets_json: Dict
    ) -> List[EventTicketForSale]:
        ticketswap_tickets: Tickets = Tickets(**event_tickets_json)

        try:
            for (
                public_listing
            ) in ticketswap_tickets.page_props.initial_apollo_state.public_listings:
                id = public_listing.id
                if id in [ticket.id for ticket in self.tickets_for_sale]:
                    print(f"{id} already parsed. Skipping..")
                    continue

                ticket_for_sale = EventTicketForSale(
                    updated=datetime.now(),
                    id=id,
                    description=public_listing.description,
                    amount_of_tickets=public_listing.number_of_tickets_still_for_sale,
                    original_price=self._convert_price(
                        public_listing.price.original_price.amount
                    ),
                    price=self._convert_price(
                        public_listing.price.total_price_with_transaction_fee.amount
                    ),
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
        return self.tickets_for_sale

    def parse_sold_tickets(self, sold_listings_json: Dict) -> List[EventTicketSold]:
        sold_listings_response: SoldListingsResponse = SoldListingsResponse(
            **sold_listings_json[0]["data"]["node"]
        )
        try:
            for edge in sold_listings_response.sold_listings.edges:
                id = edge.node.id
                if id in [ticket.id for ticket in self.tickets_sold]:
                    print(f"{id} already parsed. Skipping..")
                    continue

                sold_ticket = EventTicketSold(
                    updated=datetime.now(),
                    id=id,
                    description=edge.node.description,
                    amount_of_tickets=edge.node.number_of_tickets_in_listing,
                    original_price=self._convert_price(
                        edge.node.price.original_price.amount
                    ),
                    price=self._convert_price(
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
        return self.tickets_sold

    def parse_event(self, event_data_json: Dict) -> Event:
        event_data_response = EventDataResponse(**event_data_json[0]["data"]["node"])
        try:
            event_entrance_types: List[
                EventEntranceType
            ] = self._parse_event_entrance_types(event_data_response)
            event = Event(
                updated=datetime.now(),
                id=event_data_response.id,
                entrance_slug=event_data_response.slug,
                name=event_data_response.name,
                start_date=event_data_response.start_date,
                end_date=event_data_response.end_date,
                location=event_data_response.location.name,
                city=event_data_response.location.city.name,
                available_tickets=event_data_response.available_tickets_count,
                sold_tickets=event_data_response.sold_tickets_count,
                wanted_tickets=event_data_response.ticket_alerts_count,
                entrance_types=event_entrance_types,
            )
            self.events.append(event)
        except AttributeError as e:
            print(e)
        return event

    def _parse_event_entrance_types(
        self, event_data_response: EventDataResponse
    ) -> List[EventEntranceType]:
        entrance_types = []
        for edge in event_data_response.entrance_types.edges:
            entrance_type = EventEntranceType(
                id=edge.node.id,
                slug=edge.node.slug,
                title=edge.node.title,
                start_date=edge.node.start_date,
                end_date=edge.node.end_date,
                available_tickets=edge.node.available_tickets_count,
            )
            entrance_types.append(entrance_type)
        return entrance_types

    def _convert_price(self, price) -> float:
        """Convert price amount in cents to decimal"""
        return float(price / 100)

    def store_events(self, path: str):
        with open(path, "r") as f_read:
            events = json.load(f_read)
            event_ids = [event.id for event in self.events]
            for event in events:
                if event["id"] not in event_ids:
                    self.events.append(Event(**event))

        with open(path, "w", encoding="utf-8") as f_write:
            json.dump(
                [event.dict() for event in self.events],
                f_write,
                ensure_ascii=False,
                indent=4,
                default=str,
            )

    def store_tickets_for_sale(self, path: str):
        with open(path, "r") as f_read:
            tickets = json.load(f_read)
            ticket_for_sale_ids = [ticket.id for ticket in self.tickets_for_sale]
            for ticket in tickets:
                if ticket["id"] not in ticket_for_sale_ids:
                    self.tickets_for_sale.append(EventTicketForSale(**ticket))

        with open(path, "w", encoding="utf-8") as f_write:
            json.dump(
                [ticket.dict() for ticket in self.tickets_for_sale],
                f_write,
                ensure_ascii=False,
                indent=4,
                default=str,
            )

    def store_tickets_sold(self, path: str):
        with open(path, "r") as f_read:
            tickets = json.load(f_read)
            ticket_sold_ids = [ticket.id for ticket in self.tickets_sold]
            for ticket in tickets:
                if ticket["id"] not in ticket_sold_ids:
                    self.tickets_sold.append(EventTicketSold(**ticket))

        with open(path, "w", encoding="utf-8") as f_write:
            json.dump(
                [ticket.dict() for ticket in self.tickets_sold],
                f_write,
                ensure_ascii=False,
                indent=4,
                default=str,
            )
