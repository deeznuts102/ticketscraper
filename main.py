from datetime import datetime

from scrape.scraper import (
    crawl_event,
    crawl_events,
    parse_events,
    parse_festival_season_events,
    store_models,
)


def main():
    res = crawl_events()
    nearby_events = parse_festival_season_events(res)
    events = []
    for nearby_event in nearby_events:
        res = crawl_event(nearby_event.id)
        event = parse_events(res)
        events.append(event)

    today = datetime.now().date()
    store_models(f"output/{today}.json", events)


if __name__ == "__main__":
    main()
