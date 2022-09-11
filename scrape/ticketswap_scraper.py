from typing import List
import json

from models.custom.event_tickets import EventTicketsParser
from models.rest.event_info_redirect import EventInfoRedirect, SingleEntranceType
from models.graphql.nearby_events import NearbyEvents
from models.rest.event_info import EntranceType, EventInfo

from scrape.html.html_scraper import HTMLScraper
from scrape.graphql.graphql_scraper import GraphQLScraper
from scrape.rest.rest_scraper import RestScraper


class TicketSwapScraper:
    def __init__(self):
        self.html_scraper = HTMLScraper()
        self.graphql_scraper = GraphQLScraper()
        self.rest_scraper = RestScraper()
        self.ticket_parser = EventTicketsParser()


    def scrape_weekend_tickets(self):
        session_id = self.html_scraper.get_session_id()
        events_json = self.graphql_scraper.get_events_this_weekend()[0]
        events = NearbyEvents(**events_json).get_events()
        for event in events:
            event_info_json = self.rest_scraper.get_event_info(session_id, event.slug, event.uri_id)
            # if the response contains a 'REDIRECT' message, there is only one entrance type, which is fully provided in the redirect URL
            if 'REDIRECT' in str(event_info_json):
                entrance_type: SingleEntranceType = EventInfoRedirect(**(event_info_json)).get_entrance_type()
                event_tickets_json = self.rest_scraper.get_event_tickets(session_id, event.slug, event.uri_id, entrance_type.slug, entrance_type.id)
                self.ticket_parser.parse(event_tickets_json)
            else:
                # if there are multiple entrance types, we have to get the entrance url id from the html page first for each one
                # since this is not provided in the graphql-, nor the rest-requests
                entrance_types: List[EntranceType] = EventInfo(**event_info_json).get_entrance_types()
                for entrance_type in entrance_types:
                    if entrance_type.available_tickets > 0:
                        entrance_type_id: str = self.html_scraper.get_event_entrance_type_ids(event.uri_path, event.uri_id, entrance_type.slug)
                        event_tickets_json = self.rest_scraper.get_event_tickets(session_id, event.slug, event.uri_id, entrance_type.slug, entrance_type_id)
                        self.ticket_parser.parse(event_tickets_json)

        self.ticket_parser.store_available_tickets("output/tickets.json")
