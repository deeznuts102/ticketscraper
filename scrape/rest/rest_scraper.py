
from typing import Dict, List
import requests  # type: ignore
import json

BASE_API_URL = "https://www.ticketswap.com/_next/data"

class RestScraper:

    def get_event_info(self, session_id: str, event_slug: str, event_uri_id: str) -> List[str]:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.ticketswap.com/browse/today',
            'x-nextjs-data': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        url = f"{BASE_API_URL}/{session_id}/en/event/{event_slug}/{event_uri_id}.json?eventSlug={event_slug}&eventIdOrEventTypeSlug={event_uri_id}"
        response = requests.request("POST", url, headers=headers)

        return json.loads(response.text)

    def get_event_tickets(self, session_id: str, event_slug: str, event_uri_id: str, entrance_slug: str, entrance_type_id: int) -> List[str]:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.ticketswap.com/browse/today',
            'x-nextjs-data': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        url = f"{BASE_API_URL}/{session_id}/en/event/{event_slug}/{entrance_slug}/{event_uri_id}/{entrance_type_id}.json?eventSlug={event_slug}&eventId={event_uri_id}&eventIdOrEventTypeSlug={entrance_slug}"
        response = requests.request("POST", url, headers=headers)

        return json.loads(response.text)
