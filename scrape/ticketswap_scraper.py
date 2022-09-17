from models.custom.event_parser import EventParser
from models.graphql.nearby_events import NearbyEvents

from scrape.html.html_scraper import HTMLScraper
from scrape.graphql.graphql_scraper import City, GraphQLScraper
from scrape.rest.rest_scraper import RestScraper


class TicketSwapScraper:
    def __init__(self):
        self.html_scraper = HTMLScraper()
        self.graphql_scraper = GraphQLScraper()
        self.rest_scraper = RestScraper()
        self.ticket_parser = EventParser()

    def scrape_weekend_tickets(self):
        session_id = self.html_scraper.get_session_id()
        events_json = self.graphql_scraper.get_popular_events(City.AMSTERDAM)[0]
        nearby_events = NearbyEvents(**events_json).get_events()
        for nearby_event in nearby_events:
            event_data_json = self.graphql_scraper.get_event_data(nearby_event.id)
            event = self.ticket_parser.parse_event(event_data_json)
            for entrance_type in event.entrance_types:
                # scrape available tickets
                if entrance_type.available_tickets > 0:
                    # need to fetch the entrance type id from the HTML page in order to ge the available tickets, this is not avaialble in the Graphql or REST responses
                    entrance_type_url_id: str = (
                        self.html_scraper.get_event_entrance_type_ids(
                            nearby_event.uri_path,
                            nearby_event.uri_id,
                            entrance_type.slug,
                        )
                    )
                    event_tickets_json = self.rest_scraper.get_available_tickets(
                        session_id,
                        nearby_event.slug,
                        nearby_event.uri_id,
                        entrance_type.slug,
                        entrance_type_url_id,
                    )
                    self.ticket_parser.parse_available_tickets(event_tickets_json)

                # scrape sold tickets
                sold_listings_json = self.graphql_scraper.get_sold_listings(
                    entrance_type.id
                )
                self.ticket_parser.parse_sold_tickets(sold_listings_json)

        self.ticket_parser.store("output/result.json")
