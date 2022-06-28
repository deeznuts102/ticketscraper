from datetime import datetime
from models.helper import store_models
from models.ticket import extract_tickets

from scrape.scraper import (
    crawl_event,
    crawl_events,
    parse_events,
    parse_festival_season_events,
)


def main():
    res = crawl_events()
    nearby_events = parse_festival_season_events(res)
    events = []
    for nearby_event in nearby_events:
        res = crawl_event(nearby_event.id)
        event = parse_events(res)
        events.append(event)

    tickets = extract_tickets(events)

    today = datetime.now().date()
    store_models(f"output/tickets/{today}.json", tickets)


if __name__ == "__main__":
    main()
