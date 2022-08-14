from datetime import datetime
from typing import List
from models.event import Event
from models.helper import store_models
from models.ticket import extract_tickets

from scrape.scraper import (
    get_event_structure_data,
    get_nearby_events,
    parse_events,
    parse_festival_season_events,
    parse_nearby_events,
    get_reserved_listings,
    parse_reserved_listings,
    parse_structured_event_data,
)


def main():
    res = get_nearby_events()
    # nearby_events = parse_festival_season_events(res)
    nearby_events = parse_nearby_events(res)
    nearby_event_ids = nearby_events.get_explore_feed_event_ids()

    events: List[Event] = []
    for nearby_event_id in nearby_event_ids:
        # res = get_reserved_listings(id)
        res_json = get_event_structure_data(nearby_event_id)
        event_data = parse_structured_event_data(res_json)
        event_ids = event_data.get_event_ids()
        for event_id in event_ids:
            res = get_reserved_listings(event_id)
            listings = parse_reserved_listings(res)

        # listing = parse_reserved_listings(res)
        # event = parse_events(res)
        events.append(event_data)

    tickets = extract_tickets(events)

    today = datetime.now().date()
    store_models(f"output/tickets/{today}.json", tickets)


if __name__ == "__main__":
    main()
